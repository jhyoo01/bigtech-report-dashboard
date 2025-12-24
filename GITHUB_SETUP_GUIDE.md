# 🚀 GitHub Pages 배포 완벽 가이드

## 📋 목차
1. [GitHub 저장소 생성](#1-github-저장소-생성)
2. [파일 업로드](#2-파일-업로드)
3. [GitHub Pages 활성화](#3-github-pages-활성화)
4. [자동 업데이트 설정](#4-자동-업데이트-설정-선택)
5. [확인 및 테스트](#5-확인-및-테스트)

---

## 1. GitHub 저장소 생성

### 방법 A: GitHub 웹사이트에서 생성

1. https://github.com 접속 및 로그인
2. 오른쪽 상단 `+` 버튼 클릭 → `New repository`
3. 저장소 정보 입력:
   - **Repository name**: `bigtech-report-dashboard`
   - **Description**: `📊 빅테크 기업 뉴스 분석 대시보드`
   - **Public** 선택 (GitHub Pages는 Public 저장소에서 무료)
   - ✅ **Add a README file** 체크
   - **License**: MIT License 선택 (선택사항)
4. `Create repository` 클릭

### 방법 B: GitHub CLI 사용

```bash
# GitHub CLI 설치 필요 (https://cli.github.com/)
gh repo create bigtech-report-dashboard --public --description "📊 빅테크 기업 뉴스 분석 대시보드"
```

---

## 2. 파일 업로드

### 방법 A: GitHub 웹 인터페이스 (초보자 권장)

1. 생성한 저장소 페이지로 이동
2. `Add file` → `Upload files` 클릭
3. 다음 파일/폴더를 드래그 앤 드롭:
   ```
   ├── docs/
   │   ├── index.html
   │   ├── data/
   │   │   └── bigtech_data_latest.json
   │   ├── scripts/
   │   │   └── run_bigtech_crawler.py
   │   └── README.md
   ├── .github/
   │   └── workflows/
   │       └── update-data.yml
   ├── DEPLOY_GUIDE.md
   └── README.md
   ```
4. 하단에 커밋 메시지 입력: `Initial commit: Add BigTech Dashboard`
5. `Commit changes` 클릭

### 방법 B: Git 명령어 (개발자 권장)

```bash
# 1. 로컬에 저장소 클론
git clone https://github.com/[사용자명]/bigtech-report-dashboard.git
cd bigtech-report-dashboard

# 2. 다운로드 받은 파일들을 이 폴더에 복사
# (docs/, .github/ 폴더와 모든 파일)

# 3. Git에 추가
git add .
git commit -m "Initial commit: Add BigTech Dashboard"

# 4. GitHub에 푸시
git push origin main
```

---

## 3. GitHub Pages 활성화

### 단계별 설정

1. **저장소의 Settings 탭** 이동
   
2. 왼쪽 메뉴에서 **"Pages"** 클릭

3. **Source 섹션** 설정:
   - **Branch**: `main` (또는 `master`) 선택
   - **Folder**: `/docs` 선택
   - **Save** 클릭

4. **확인**:
   - 페이지 상단에 초록색 박스가 나타납니다:
   ```
   Your site is published at https://[사용자명].github.io/bigtech-report-dashboard/
   ```

5. **대기**:
   - 첫 배포는 1-2분 정도 소요됩니다
   - 상단의 링크를 클릭하여 사이트 접속

### 배포 상태 확인

- **Actions 탭**에서 배포 진행 상황 확인 가능
- 초록색 체크 표시가 나타나면 배포 완료

---

## 4. 자동 업데이트 설정 (선택)

GitHub Actions를 사용하여 매일 자동으로 뉴스 데이터를 업데이트할 수 있습니다.

### 워크플로우 활성화

`.github/workflows/update-data.yml` 파일이 이미 포함되어 있습니다.

### 수동 실행 테스트

1. 저장소의 **Actions** 탭 이동
2. 왼쪽에서 **"Update BigTech News Data"** 선택
3. 오른쪽 **"Run workflow"** 버튼 클릭
4. 드롭다운에서 `main` 브랜치 선택
5. **"Run workflow"** 클릭

### 자동 실행 스케줄

기본 설정:
- **매일 오전 9시(KST)** 자동 실행
- UTC 기준 0시 (= KST 9시)

스케줄 변경하려면 `.github/workflows/update-data.yml` 수정:
```yaml
on:
  schedule:
    # 예: 매일 오전 6시(KST) 실행하려면
    - cron: '0 21 * * *'  # UTC 21시 = KST 6시
```

### Cron 표현식 참고

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── 요일 (0-7, 0과 7은 일요일)
│ │ │ └───── 월 (1-12)
│ │ └─────── 일 (1-31)
│ └───────── 시 (0-23, UTC 기준)
└─────────── 분 (0-59)
```

예시:
- `0 0 * * *` - 매일 자정(UTC)
- `0 */6 * * *` - 6시간마다
- `0 0 * * 1` - 매주 월요일 자정

---

## 5. 확인 및 테스트

### 사이트 접속

```
https://[사용자명].github.io/bigtech-report-dashboard/
```

예: `https://jhyoo01.github.io/bigtech-report-dashboard/`

### 테스트 체크리스트

- [ ] 사이트가 정상적으로 로드됨
- [ ] "최신 데이터 로드" 버튼 작동
- [ ] "샘플 데이터 보기" 버튼 작동
- [ ] 차트가 정상적으로 표시됨
- [ ] 뉴스 카드 클릭 시 링크 열림
- [ ] 모바일에서도 정상 작동

### 문제 해결

**사이트가 404 에러:**
- Settings → Pages에서 Source가 올바르게 설정되었는지 확인
- `/docs` 폴더가 저장소에 존재하는지 확인
- 1-2분 정도 대기 후 다시 시도

**데이터가 로드되지 않음:**
- `docs/data/bigtech_data_latest.json` 파일이 존재하는지 확인
- 브라우저 콘솔(F12)에서 에러 메시지 확인
- JSON 파일 형식이 올바른지 확인

**GitHub Actions가 실행되지 않음:**
- Actions 탭에서 워크플로우가 활성화되어 있는지 확인
- 저장소 Settings → Actions → General에서 권한 확인
- "Allow all actions and reusable workflows" 선택

---

## 6. 데이터 업데이트 방법

### 로컬에서 업데이트

```bash
# 1. 저장소 클론 (처음 한 번만)
git clone https://github.com/[사용자명]/bigtech-report-dashboard.git
cd bigtech-report-dashboard

# 2. 크롤러 실행
python3 docs/scripts/run_bigtech_crawler.py

# 3. 최신 데이터 파일 복사
cp bigtech_data_*.json docs/data/bigtech_data_latest.json

# 4. GitHub에 업로드
git add docs/data/bigtech_data_latest.json
git commit -m "Update news data $(date +'%Y-%m-%d')"
git push origin main
```

### 웹에서 직접 업데이트

1. GitHub 저장소에서 `docs/data/bigtech_data_latest.json` 파일 클릭
2. 연필 아이콘(Edit) 클릭
3. 내용 붙여넣기
4. 하단에서 "Commit changes" 클릭

---

## 🎉 완료!

이제 다음 작업을 할 수 있습니다:

✅ 사이트가 `https://[사용자명].github.io/bigtech-report-dashboard/`에서 실행 중
✅ 언제든지 데이터를 업데이트할 수 있음
✅ GitHub Actions로 자동 업데이트 가능
✅ 모든 코드가 GitHub에 백업됨

---

## 📚 추가 리소스

- [GitHub Pages 공식 문서](https://docs.github.com/en/pages)
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [Chart.js 문서](https://www.chartjs.org/docs/)

---

## 💡 팁

1. **커스텀 도메인 연결**:
   - Settings → Pages → Custom domain에서 설정 가능
   
2. **HTTPS 강제**:
   - Settings → Pages에서 "Enforce HTTPS" 체크

3. **README 배지 추가**:
   ```markdown
   ![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)
   ```

4. **분석 추가**:
   - Google Analytics 코드를 `docs/index.html`에 추가

---

**문제가 발생하면 GitHub Issues에서 질문해주세요!** 🚀
