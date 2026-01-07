# 📊 글비 빅테크 리포트 대시보드

<div align="center">

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success?style=for-the-badge&logo=github)](https://jhyoo01.github.io/bigtech-report-dashboard/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Google, Meta, YouTube, TikTok, PayPal, Microsoft, Amazon의 최신 뉴스를 수집하고 분석하는 종합 대시보드**

[🚀 라이브 데모](https://jhyoo01.github.io/bigtech-report-dashboard/) | [📖 문서](DEPLOY_GUIDE.md) | [🐛 버그 리포트](https://github.com/jhyoo01/bigtech-report-dashboard/issues)

</div>
 
---

## ✨ 주요 기능

- 🔍 **7개 빅테크 기업** 실시간 뉴스 모니터링
- 📊 **인터랙티브 차트** Chart.js 기반 시각화
- ⭐ **AI 중요도 점수** 자동 계산 (0-100점)
- 📑 **자동 카테고리 분류** 7가지 카테고리
- 💾 **다중 포맷 지원** JSON, CSV, Markdown
- 🎨 **반응형 디자인** 모바일/데스크톱 최적화
- 🤖 **GitHub Actions** 자동 데이터 업데이트

## 🎯 수집 대상 기업

<table>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Google-4285F4?style=for-the-badge&logo=google&logoColor=white"/></td>
<td align="center"><img src="https://img.shields.io/badge/Meta-0668E1?style=for-the-badge&logo=meta&logoColor=white"/></td>
<td align="center"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"/></td>
<td align="center"><img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white"/></td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/PayPal-003087?style=for-the-badge&logo=paypal&logoColor=white"/></td>
<td align="center"><img src="https://img.shields.io/badge/Microsoft-00A4EF?style=for-the-badge&logo=microsoft&logoColor=white"/></td>
<td align="center"><img src="https://img.shields.io/badge/Amazon-FF9900?style=for-the-badge&logo=amazon&logoColor=white"/></td>
<td align="center"></td>
</tr>
</table>

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/jhyoo01/bigtech-report-dashboard.git
cd bigtech-report-dashboard
```

### 2. 로컬에서 실행

```bash
# Python 내장 서버 사용
cd docs
python3 -m http.server 8000

# 브라우저에서 접속
# http://localhost:8000
```

### 3. 데이터 수집

```bash
# 크롤러 실행
python3 docs/scripts/run_bigtech_crawler.py

# 생성된 JSON 파일을 최신 데이터로 복사
cp bigtech_data_*.json docs/data/bigtech_data_latest.json
```

## 📁 프로젝트 구조

```
bigtech-report-dashboard/
├── docs/                           # GitHub Pages 루트
│   ├── index.html                  # 메인 대시보드
│   ├── data/
│   │   └── bigtech_data_latest.json
│   └── scripts/
│       └── run_bigtech_crawler.py
├── .github/
│   └── workflows/
│       └── update-data.yml         # 자동 업데이트 워크플로우
├── README.md
├── DEPLOY_GUIDE.md
└── LICENSE
```

## 🌐 GitHub Pages 배포

### 자동 배포 (권장)

1. GitHub 저장소 생성
2. 코드를 Push
3. Settings → Pages → Source를 `main` 브랜치의 `/docs` 폴더로 설정
4. 약 1-2분 후 `https://[username].github.io/bigtech-report-dashboard/` 접속

### 자동 업데이트 설정

GitHub Actions가 자동으로 설정되어 있습니다:
- **일정**: 매일 오전 9시(KST) 자동 실행
- **수동**: Actions 탭에서 "Run workflow" 클릭

## 📊 데이터 포맷

### JSON 구조

```json
{
  "timestamp": "2025-12-24T01:04:05.921523",
  "statistics": {
    "Google_count": 2,
    "Meta_count": 1,
    ...
  },
  "news": {
    "Google": [
      {
        "title": "뉴스 제목",
        "url": "https://...",
        "snippet": "요약",
        "source": "출처",
        "published_date": "2025-12-24",
        "category": "Product Launch",
        "importance_score": 80.0
      }
    ]
  }
}
```

## 📑 뉴스 카테고리

| 카테고리 | 설명 | 키워드 예시 |
|---------|------|------------|
| 🚀 Product Launch | 제품 출시 | launch, release, unveil |
| 💰 Financial Results | 실적 발표 | revenue, earnings, profit |
| ⚖️ Regulation & Policy | 규제 및 정책 | regulation, law, antitrust |
| 🔬 Technology Innovation | 기술 혁신 | AI, innovation, patent |
| 🥊 Competition | 경쟁 동향 | compete, rival, battle |
| 👔 Leadership & Strategy | 임원 및 전략 | CEO, executive, strategy |
| 📈 Market Trends | 시장 트렌드 | trend, growth, expansion |

## 🎨 커스터마이징

### 기업 추가

`docs/scripts/run_bigtech_crawler.py` 수정:

```python
COMPANIES = {
    'Tesla': {
        'keywords': ['Tesla', 'Elon Musk'],
        'emoji': '🚗',
        'color': '#E31937'
    },
    # 기존 기업들...
}
```

### 스타일 변경

`docs/index.html`의 `<style>` 섹션에서:
- 배경 그라데이션
- 카드 색상
- 폰트 크기
등을 수정 가능

## 🛠️ 기술 스택

| 카테고리 | 기술 |
|---------|------|
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| Visualization | Chart.js 4.4.0 |
| Backend | Python 3.10+ |
| Deployment | GitHub Pages, GitHub Actions |
| Data Format | JSON, CSV, Markdown |

## 📈 로드맵

- [ ] 실시간 뉴스 API 연동
- [ ] 감성 분석 추가
- [ ] 다국어 지원 (영어, 한국어)
- [ ] 뉴스 알림 기능
- [ ] 데이터 히스토리 그래프
- [ ] PWA 지원

## 🤝 기여하기

기여는 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👨‍💻 개발자

**Glovy** - [@jhyoo01](https://github.com/jhyoo01)

프로젝트 링크: [https://github.com/jhyoo01/bigtech-report-dashboard](https://github.com/jhyoo01/bigtech-report-dashboard)

## 🙏 감사의 말

- [Chart.js](https://www.chartjs.org/) - 차트 라이브러리
- [GitHub Pages](https://pages.github.com/) - 무료 호스팅
- [Font Awesome](https://fontawesome.com/) - 아이콘

---

<div align="center">

**Made with ❤️ for Big Tech News Monitoring**

⭐ 이 프로젝트가 마음에 드셨다면 Star를 눌러주세요!

</div>
