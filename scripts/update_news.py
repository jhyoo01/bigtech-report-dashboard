#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BigTech News Updater for GitHub Pages
실제 빅테크 뉴스를 크롤링하고 bigtech_data_latest.json을 업데이트합니다.
"""

import os
import re
import json
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import quote_plus, urlparse
import hashlib


class BigTechNewsUpdater:
    """빅테크 뉴스 자동 업데이트"""
    
    def __init__(self):
        self.news_data = {}
        self.all_news = []
        self.companies = {
            'Google': ['Google', 'Alphabet', 'Sundar Pichai'],
            'Meta': ['Meta', 'Facebook', 'Instagram', 'Mark Zuckerberg'],
            'YouTube': ['YouTube', 'YouTube Premium'],
            'TikTok': ['TikTok', 'ByteDance'],
            'PayPal': ['PayPal', 'Venmo'],
            'Stripe': ['Stripe', 'Patrick Collison'],
            'Microsoft': ['Microsoft', 'Satya Nadella', 'Azure'],
            'Amazon': ['Amazon', 'AWS', 'Andy Jassy']
        }
        
        for company in self.companies.keys():
            self.news_data[company] = []
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.target_sources = ['theverge.com', 'techcrunch.com']  # 주요 출처
        self.seen_hashes = set()
    
    def translate_to_korean(self, text):
        """Google Translate API를 사용한 한글 번역"""
        if not text or len(text.strip()) == 0:
            return text
        
        try:
            # Google Translate 무료 API 사용
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',  # source language: English
                'tl': 'ko',  # target language: Korean
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                result = response.json()
                # 번역된 텍스트 추출
                translated = ''.join([item[0] for item in result[0] if item[0]])
                return translated
            else:
                return text
        except Exception as e:
            print(f"    번역 오류: {e}")
            return text
    
    def is_duplicate(self, title):
        """중복 체크"""
        title_hash = hashlib.md5(title.encode()).hexdigest()
        if title_hash in self.seen_hashes:
            return True
        self.seen_hashes.add(title_hash)
        return False
    
    def search_bigtech_news(self):
        """실제 빅테크 뉴스 검색"""
        print("🔍 빅테크 뉴스 검색 중...")
        
        for company, keywords in self.companies.items():
            print(f"\n📱 {company} 뉴스 수집 중...")
            company_news = []
            
            for keyword in keywords[:2]:  # 주요 키워드 2개만
                try:
                    print(f"  검색 중: {keyword}")
                    news = self.fetch_real_news(keyword, company, max_items=25)
                    company_news.extend(news)
                    time.sleep(0.5)
                except Exception as e:
                    print(f"⚠️  {keyword} 검색 실패: {e}")
            
            # 정렬: 우선 출처 > 최신순
            def sort_key(n):
                is_priority = any(s in n.get('url', '').lower() for s in self.target_sources)
                priority = 0 if is_priority else 1
                return (priority, n.get('published_date', '2000-01-01'))
            
            company_news.sort(key=sort_key, reverse=True)
            self.news_data[company] = company_news[:50]  # 최대 50개
            
            print(f"  ✅ {len(self.news_data[company])}개 수집 완료")
            
            # 우선 출처 통계
            priority_count = sum(1 for n in self.news_data[company] 
                               if any(s in n.get('url', '').lower() for s in self.target_sources))
            print(f"  📰 우선 출처: {priority_count}개")
    
    def fetch_real_news(self, keyword, company, max_items=25):
        """실제 뉴스 검색 (Google News RSS 활용)"""
        news_items = []
        
        try:
            # Google News RSS 피드 사용
            rss_url = f"https://news.google.com/rss/search?q={quote_plus(keyword)}&hl=en-US&gl=US&ceid=US:en"
            
            response = requests.get(rss_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return news_items
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:max_items * 2]
            
            for item in items:
                try:
                    title = item.title.text if item.title else ""
                    link = item.link.text if item.link else ""
                    pub_date = item.pubDate.text if item.pubDate else ""
                    description = item.description.text if item.description else ""
                    source_tag = item.source.text if item.source else "News"
                    
                    # 중복 체크
                    if self.is_duplicate(title):
                        continue
                    
                    # 발행 날짜 파싱 및 14일 필터링
                    from email.utils import parsedate_to_datetime
                    try:
                        pub_datetime = parsedate_to_datetime(pub_date)
                        now = datetime.now(pub_datetime.tzinfo)
                        days_old = (now - pub_datetime).days
                        
                        # 14일 이상 된 뉴스는 스킵
                        if days_old > 14:
                            continue
                        
                        actual_date = pub_datetime.strftime('%Y-%m-%d')
                    except:
                        actual_date = datetime.now().strftime('%Y-%m-%d')
                        days_old = 0
                    
                    # 회사명 관련성 체크
                    title_lower = title.lower()
                    if not any(kw.lower() in title_lower for kw in self.companies[company]):
                        continue
                    
                    # 출처 도메인 추출
                    try:
                        domain = urlparse(link).netloc.replace('www.', '')
                        source = domain if domain else source_tag
                    except:
                        source = source_tag
                    
                    # 우선 출처 확인
                    is_target_source = any(target in link.lower() for target in self.target_sources)
                    
                    # 설명 정제
                    description_clean = BeautifulSoup(description, 'html.parser').get_text()
                    description_clean = description_clean[:200] + "..." if len(description_clean) > 200 else description_clean
                    
                    # 카테고리 분류
                    category = self.classify_category(title + " " + description_clean)
                    
                    # 중요도 계산
                    importance = self.calculate_importance(title, source, is_target_source)
                    
                    # 한글 번역
                    print(f"    번역 중: {title[:50]}... ({days_old}일 전)")
                    title_ko = self.translate_to_korean(title)
                    snippet_ko = self.translate_to_korean(description_clean) if description_clean else ""
                    
                    news_items.append({
                        'title': title,
                        'title_ko': title_ko,
                        'url': link,
                        'snippet': description_clean,
                        'snippet_ko': snippet_ko,
                        'source': source,
                        'published_date': actual_date,
                        'category': category,
                        'importance_score': importance,
                        'company': company
                    })
                    
                    if len(news_items) >= max_items:
                        break
                    
                    time.sleep(0.3)  # 번역 API rate limit 방지
                    
                except Exception as e:
                    print(f"    항목 처리 실패: {e}")
                    continue
                    
        except Exception as e:
            print(f"  RSS 피드 가져오기 실패: {e}")
        
        return news_items
    
    def classify_category(self, text):
        """카테고리 자동 분류"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['launch', 'release', 'unveil', 'announce']):
            return 'Product Launch'
        elif any(word in text_lower for word in ['revenue', 'earnings', 'profit', 'stock']):
            return 'Financial Results'
        elif any(word in text_lower for word in ['regulation', 'law', 'lawsuit', 'fine', 'court']):
            return 'Regulation & Policy'
        elif any(word in text_lower for word in ['ai', 'artificial intelligence', 'technology', 'innovation']):
            return 'Technology Innovation'
        elif any(word in text_lower for word in ['compete', 'rival', 'versus', 'market share']):
            return 'Competition'
        elif any(word in text_lower for word in ['ceo', 'executive', 'appoint', 'resign']):
            return 'Leadership & Strategy'
        else:
            return 'Market Trends'
    
    def calculate_importance(self, title, source, is_target_source=False):
        """중요도 점수 계산"""
        score = 50.0
        
        # 우선 출처 가중치
        if is_target_source:
            score += 25.0
        
        # 제목 키워드 가중치
        title_lower = title.lower()
        high_impact = ['billion', 'acquisition', 'launch', 'announces', 'breakthrough', 'major']
        for word in high_impact:
            if word in title_lower:
                score += 10.0
                break
        
        # 출처 가중치
        premium_sources = ['TechCrunch', 'The Verge', 'Bloomberg', 'Reuters', 'CNBC']
        if any(s.lower() in source.lower() for s in premium_sources):
            score += 10.0
        
        return min(100.0, round(score, 1))
    
    def generate_json(self):
        """JSON 데이터 생성"""
        print("\n📝 JSON 생성 중...")
        
        stats = {}
        for company, articles in self.news_data.items():
            stats[f'{company}_count'] = len(articles)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'news': self.news_data,
            'metadata': {
                'total_articles': sum(stats.values()),
                'companies': list(self.companies.keys()),
                'collection_date': datetime.now().strftime('%Y-%m-%d'),
                'cutoff_days': 14,
                'priority_sources': self.target_sources,
                'generated_by': 'BigTech News Crawler v1.0'
            }
        }
        
        return data
    
    def save_json(self, data):
    """JSON 파일 저장"""
    # 디렉토리 생성
    os.makedirs('data', exist_ok=True)
    
    # data 폴더에 저장
    filepath = 'data/bigtech_data_latest.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {filepath} 업데이트 완료!")
    
    def run(self):
        """전체 프로세스 실행"""
        print("🚀 BigTech News Updater 시작...")
        print("=" * 60)
        
        try:
            # 1. 뉴스 수집
            self.search_bigtech_news()
            
            # 2. JSON 생성
            data = self.generate_json()
            
            # 3. 저장
            self.save_json(data)
            
            print("\n" + "=" * 60)
            print("✨ 업데이트 완료!")
            print(f"📅 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 총 {data['metadata']['total_articles']}개 기사")
            
            # 기업별 통계
            print("\n📊 기업별 통계:")
            for company, count in data['statistics'].items():
                print(f"  {company}: {count}")
            
            # 뉴스 미리보기
            print("\n📰 수집된 뉴스 미리보기:")
            count = 0
            for company, articles in self.news_data.items():
                for article in articles[:2]:
                    count += 1
                    print(f"{count}. [{article['source']}] {article['title_ko'][:60]}...")
                    if count >= 5:
                        break
                if count >= 5:
                    break
            
            return 0
        
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """메인 실행"""
    updater = BigTechNewsUpdater()
    return updater.run()


if __name__ == "__main__":
    exit(main())
