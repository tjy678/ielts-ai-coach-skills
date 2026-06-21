"""IELTS Dashboard 本地静态服务器 - 端口 8765

支持 GET 静态文件 + POST /api/save 数据持久化 + POST /api/analysis 模考解读报告管理。
"""
import http.server
import socketserver
import os
import json
import urllib.parse
import re

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'analysis-reports')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = BASE_DIR
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_POST(self):
        """Handle POST endpoints"""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/api/save':
            self._handle_save()
        elif parsed.path == '/api/analysis/save':
            self._handle_analysis_save()
        elif parsed.path == '/api/analysis/save-report':
            self._handle_analysis_save_report()
        elif parsed.path == '/api/analysis/list':
            self._handle_analysis_list()
        elif parsed.path == '/api/writing/save-score':
            self._handle_writing_save_score()
        elif parsed.path == '/api/analysis/delete':
            self._handle_analysis_delete()
        else:
            self._json_response(404, {'ok': False, 'error': 'Not found'})

    def _handle_save(self):
        """POST /api/save — persist JSON to disk"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            file_path = payload.get('path', '')
            data = payload.get('data')

            if not file_path or data is None:
                self._json_response(400, {'ok': False, 'error': 'Missing path or data'})
                return

            full_path = os.path.normpath(os.path.join(BASE_DIR, file_path))
            # Case-insensitive path check for Windows compatibility
            if not full_path.lower().startswith(os.path.normpath(DATA_DIR).lower()):
                self._json_response(403, {'ok': False, 'error': 'Access denied: must write under data/'})
                return

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self._json_response(200, {'ok': True, 'path': file_path})
        except json.JSONDecodeError:
            self._json_response(400, {'ok': False, 'error': 'Invalid JSON'})
        except Exception as e:
            self._json_response(500, {'ok': False, 'error': str(e)})

    def _handle_analysis_save(self):
        """POST /api/analysis/save — save analysis report as markdown file"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            filename = payload.get('filename', '')
            content = payload.get('content', '')

            if not filename or not content:
                self._json_response(400, {'ok': False, 'error': 'Missing filename or content'})
                return

            # Security: only allow .md files, sanitize filename
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', filename)
            if not safe_name.endswith('.md'):
                safe_name += '.md'

            full_path = os.path.normpath(os.path.join(REPORTS_DIR, safe_name))
            if not full_path.startswith(os.path.normpath(REPORTS_DIR)):
                self._json_response(403, {'ok': False, 'error': 'Access denied'})
                return

            os.makedirs(REPORTS_DIR, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self._json_response(200, {'ok': True, 'path': 'analysis-reports/' + safe_name})
        except Exception as e:
            self._json_response(500, {'ok': False, 'error': str(e)})

    def _handle_analysis_save_report(self):
        """POST /api/analysis/save-report — AI skill backfills analysis report and updates exam status"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            exam_id = payload.get('examId', '')
            filename = payload.get('filename', '')
            content = payload.get('content', '')
            timestamp = payload.get('timestamp', '')

            if not exam_id or not content:
                self._json_response(400, {'ok': False, 'error': 'Missing examId or content'})
                return

            # 1. Save the report file
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', filename or f'{exam_id}.md')
            if not safe_name.endswith('.md'):
                safe_name += '.md'

            full_path = os.path.normpath(os.path.join(REPORTS_DIR, safe_name))
            if not full_path.startswith(os.path.normpath(REPORTS_DIR)):
                self._json_response(403, {'ok': False, 'error': 'Access denied'})
                return

            os.makedirs(REPORTS_DIR, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 2. Update exam record: set analysisStatus = 'scored'
            exam_idx_path = os.path.join(DATA_DIR, 'exam', 'index.json')
            if os.path.exists(exam_idx_path):
                with open(exam_idx_path, 'r', encoding='utf-8') as f:
                    exam_idx = json.load(f)

                exam_found = False
                for exam in exam_idx.get('exams', []):
                    if exam.get('id') == exam_id:
                        exam_found = True
                        exam['analysisStatus'] = 'scored'
                        exam['analysisReport'] = 'analysis-reports/' + safe_name
                        exam['analysisTimestamp'] = timestamp or ''
                        break

                if exam_found:
                    with open(exam_idx_path, 'w', encoding='utf-8') as f:
                        json.dump(exam_idx, f, ensure_ascii=False, indent=2)

            self._json_response(200, {
                'ok': True,
                'examId': exam_id,
                'filename': safe_name,
                'path': 'analysis-reports/' + safe_name
            })

        except json.JSONDecodeError:
            self._json_response(400, {'ok': False, 'error': 'Invalid JSON'})
        except Exception as e:
            self._json_response(500, {'ok': False, 'error': str(e)})

    def _handle_analysis_delete(self):
        """POST /api/analysis/delete — delete an analysis report file"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            filename = payload.get('filename', '')
            if not filename:
                self._json_response(400, {'ok': False, 'error': 'Missing filename'})
                return

            safe_name = re.sub(r'[\\/:*?"<>|]', '_', filename)
            if not safe_name.endswith('.md'):
                safe_name += '.md'

            full_path = os.path.normpath(os.path.join(REPORTS_DIR, safe_name))
            if not full_path.startswith(os.path.normpath(REPORTS_DIR)):
                self._json_response(403, {'ok': False, 'error': 'Access denied'})
                return

            if os.path.exists(full_path):
                os.remove(full_path)
                self._json_response(200, {'ok': True, 'filename': safe_name})
            else:
                self._json_response(404, {'ok': False, 'error': 'File not found'})
        except Exception as e:
            self._json_response(500, {'ok': False, 'error': str(e)})

    def _handle_analysis_list(self):
        """POST /api/analysis/list — list all saved analysis reports"""
        try:
            os.makedirs(REPORTS_DIR, exist_ok=True)
            reports = []
            for fname in os.listdir(REPORTS_DIR):
                if fname.endswith('.md') and fname != 'README.md':
                    fpath = os.path.join(REPORTS_DIR, fname)
                    stat = os.stat(fpath)
                    # Extract first heading as title
                    title = fname.replace('.md', '')
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            first_line = f.readline()
                            if first_line.startswith('# '):
                                title = first_line.lstrip('# ').strip()
                    except:
                        pass
                    reports.append({
                        'filename': fname,
                        'title': title,
                        'size': stat.st_size,
                        'modified': stat.st_mtime
                    })
            reports.sort(key=lambda r: r['modified'], reverse=True)
            self._json_response(200, {'ok': True, 'reports': reports})
        except Exception as e:
            self._json_response(500, {'ok': False, 'error': str(e)})

    def _handle_writing_save_score(self):
        """POST /api/writing/save-score — AI skill writes essay scores back to exam record and writing index"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            exam_id = payload.get('examId', '')
            task_type = payload.get('taskType', '')  # 'task1' or 'task2'
            scores = payload.get('scores', {})       # { tr/ta, cc, lr, gra, overall, weakestDimension }
            rewritten_paragraphs = payload.get('rewrittenParagraphs', [])
            key_suggestions = payload.get('keySuggestions', [])
            question = payload.get('question', '')
            essay_text = payload.get('essay', '')

            if not exam_id or not task_type or not scores:
                self._json_response(400, {'ok': False, 'error': 'Missing examId, taskType, or scores'})
                return

            # Validate task_type
            if task_type not in ('task1', 'task2'):
                self._json_response(400, {'ok': False, 'error': 'taskType must be task1 or task2'})
                return

            # Sanitize exam_id against path traversal
            safe_id = ''.join(c for c in exam_id if c.isalnum() or c in '-_')
            if safe_id != exam_id:
                self._json_response(400, {'ok': False, 'error': 'examId contains invalid characters'})
                return

            # 1. Update exam record with AI scores
            exam_idx_path = os.path.join(DATA_DIR, 'exam', 'index.json')
            if not os.path.exists(exam_idx_path):
                self._json_response(404, {'ok': False, 'error': 'exam/index.json not found'})
                return

            with open(exam_idx_path, 'r', encoding='utf-8') as f:
                exam_idx = json.load(f)

            exam_found = False
            for exam in exam_idx.get('exams', []):
                if exam.get('id') == exam_id:
                    exam_found = True
                    # Ensure essayData exists
                    if 'essayData' not in exam or not exam['essayData']:
                        exam['essayData'] = {}
                    if task_type not in exam['essayData']:
                        exam['essayData'][task_type] = {}

                    # Write AI scores into essayData
                    exam['essayData'][task_type]['scores'] = scores
                    exam['essayData'][task_type]['aiScored'] = True
                    exam['essayData'][task_type]['scoredAt'] = payload.get('timestamp', '')
                    if question:
                        exam['essayData'][task_type]['question'] = question

                    # Update writingStatus
                    t1_done = exam.get('essayData', {}).get('task1', {}).get('aiScored', False)
                    t2_done = exam.get('essayData', {}).get('task2', {}).get('aiScored', False)
                    has_t1 = 'task1' in exam.get('essayData', {})
                    has_t2 = 'task2' in exam.get('essayData', {})
                    if has_t1 and has_t2:
                        exam['writingStatus'] = 'scored' if (t1_done and t2_done) else 'partial'
                    elif has_t1:
                        exam['writingStatus'] = 'scored' if t1_done else 'pending'
                    elif has_t2:
                        exam['writingStatus'] = 'scored' if t2_done else 'pending'

                    # Auto-update writing band if not manually set
                    if task_type == 'task2' and 'overall' in scores:
                        overall_w = scores['overall']
                        if exam['scores'].get('writing') is None or exam['scores']['writing'] == 0:
                            exam['scores']['writing'] = overall_w
                            # Recalculate overall
                            l = exam['scores'].get('listening')
                            r = exam['scores'].get('reading')
                            w = overall_w
                            s = exam['scores'].get('speaking')
                            vals = [v for v in [l, r, w, s] if v is not None and v > 0]
                            if vals:
                                avg = sum(vals) / len(vals)
                                # Round to 0.5 (0.25→0.5, 0.75→1.0)
                                exam['scores']['overall'] = round(avg * 2) / 2

                    break

            if not exam_found:
                self._json_response(404, {'ok': False, 'error': f'Exam {exam_id} not found'})
                return

            # Recalculate stats
            scorable = [e for e in exam_idx.get('exams', []) if e.get('scores', {}).get('overall') is not None]
            exam_idx['stats'] = {
                'totalExams': len(exam_idx.get('exams', [])),
                'bestOverall': max(e['scores']['overall'] for e in scorable) if scorable else None,
                'averageOverall': round(sum(e['scores']['overall'] for e in scorable) / len(scorable), 1) if scorable else None,
                'lastExamDate': max(e.get('timestamp', '') for e in exam_idx.get('exams', [])) if exam_idx.get('exams') else None
            }

            with open(exam_idx_path, 'w', encoding='utf-8') as f:
                json.dump(exam_idx, f, ensure_ascii=False, indent=2)

            # 2. Save to writing index and create essay record
            writing_dir = os.path.join(DATA_DIR, 'writing')
            os.makedirs(writing_dir, exist_ok=True)

            timestamp = payload.get('timestamp', '')
            essay_id = f"essay-{safe_id}-{task_type}"
            essay_file = os.path.join(writing_dir, f"{essay_id}.json")

            essay_record = {
                'id': essay_id,
                'examId': exam_id,
                'timestamp': timestamp,
                'taskType': task_type,
                'question': question,
                'essay': essay_text,
                'scores': scores,
                'weakestDimension': scores.get('weakestDimension', ''),
                'rewrittenParagraphs': rewritten_paragraphs,
                'keySuggestions': key_suggestions,
                'source': 'ai-skill'
            }

            with open(essay_file, 'w', encoding='utf-8') as f:
                json.dump(essay_record, f, ensure_ascii=False, indent=2)

            # Update writing index
            writing_idx_path = os.path.join(writing_dir, 'index.json')
            writing_idx = {'essays': []}
            if os.path.exists(writing_idx_path):
                with open(writing_idx_path, 'r', encoding='utf-8') as f:
                    writing_idx = json.load(f)

            # Upsert — use same score format as syncProgressFromExams: { tr, cc, lr, gra, overall }
            existing_idx = next((i for i, e in enumerate(writing_idx.get('essays', [])) if e.get('id') == essay_id), None)
            idx_entry = {
                'id': essay_id,
                'examId': exam_id,
                'timestamp': timestamp,
                'taskType': task_type,
                'scores': {
                    'tr': scores.get('tr') or scores.get('ta') or scores.get('taskResponse') or scores.get('taskAchievement') or 0,
                    'cc': scores.get('cc') or scores.get('coherence') or 0,
                    'lr': scores.get('lr') or scores.get('lexical') or 0,
                    'gra': scores.get('gra') or scores.get('grammar') or 0,
                    'overall': scores.get('overall') or 0
                },
                'weakestDimension': scores.get('weakestDimension', '')
            }
            if existing_idx is not None:
                writing_idx['essays'][existing_idx] = idx_entry
            else:
                writing_idx['essays'].append(idx_entry)

            with open(writing_idx_path, 'w', encoding='utf-8') as f:
                json.dump(writing_idx, f, ensure_ascii=False, indent=2)

            # 3. Update progress.json
            progress_path = os.path.join(DATA_DIR, 'progress.json')
            if os.path.exists(progress_path):
                with open(progress_path, 'r', encoding='utf-8') as f:
                    progress = json.load(f)

                w_prog = progress.get('writing', {})
                essays = writing_idx.get('essays', [])
                w_prog['totalEssays'] = len(essays)
                w_prog['task1Count'] = sum(1 for e in essays if e.get('taskType') == 'task1')
                w_prog['task2Count'] = sum(1 for e in essays if e.get('taskType') == 'task2')
                # Support both old format (score) and new format (scores.overall)
                scored = [e['scores']['overall'] if e.get('scores',{}).get('overall') else e.get('score') for e in essays if (e.get('scores',{}).get('overall') or e.get('score')) is not None]
                if scored:
                    w_prog['averageScore'] = round(sum(scored) / len(scored), 1)
                w_prog['trend'] = w_prog.get('trend', [])
                # Add trend entry
                trend_date = (timestamp or '')[:10] if timestamp else ''
                if trend_date:
                    existing_trend = next((t for t in w_prog['trend'] if t.get('date') == trend_date), None)
                    if existing_trend:
                        existing_trend['score'] = scores.get('overall')
                    else:
                        w_prog['trend'].append({'date': trend_date, 'score': scores.get('overall')})
                progress['writing'] = w_prog
                progress['updatedAt'] = timestamp or ''

                with open(progress_path, 'w', encoding='utf-8') as f:
                    json.dump(progress, f, ensure_ascii=False, indent=2)

            # Retrieve the updated writing status safely
            updated_exam = next((e for e in exam_idx['exams'] if e['id'] == exam_id), None)
            updated_writing_status = updated_exam.get('writingStatus', 'pending') if updated_exam else 'pending'

            self._json_response(200, {
                'ok': True,
                'examId': exam_id,
                'taskType': task_type,
                'writingStatus': updated_writing_status,
                'essayId': essay_id
            })

        except json.JSONDecodeError:
            self._json_response(400, {'ok': False, 'error': 'Invalid JSON'})
        except Exception as e:
            self._json_response(500, {'ok': False, 'error': str(e)})

    def _json_response(self, code, data):
        """Send a JSON response"""
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

# 确保 .json 文件有正确的 MIME 类型
MyHandler.extensions_map['.json'] = 'application/json'

print(f'\n  IELTS 备考 Dashboard 服务器已启动 (v1.0)')
print(f'  ========================================')
print(f'  地址: http://localhost:{PORT}/index.html')
print(f'  数据持久化: POST http://localhost:{PORT}/api/save')
print(f'  模考解读管理: POST http://localhost:{PORT}/api/analysis/save|list|delete')
print(f'  模考解读回填: POST http://localhost:{PORT}/api/analysis/save-report')
print(f'  写作评分回填: POST http://localhost:{PORT}/api/writing/save-score')
print(f'  按 Ctrl+C 停止服务器\n')

# Allow address reuse for quick restarts (especially on Windows)
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

with ReusableTCPServer(("", PORT), MyHandler) as httpd:
    try:
        print(f'  按 Ctrl+C 停止服务器\n')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
