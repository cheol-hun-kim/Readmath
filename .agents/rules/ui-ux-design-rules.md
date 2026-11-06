---
name: ui-ux-design-rules
description: Mandatory UI/UX Design Philosophy & Zero-Defect Implementation Rules (Zero Invisible Text, 60-30-10 Color, Typography & Leading, 3:5 Grid, 4-6-1 Logo Ratio, Semantic Tokens)
trigger: always_on
---

# [MANDATORY] UI/UX Design Philosophy & Zero-Defect Implementation Rules

당신은 수학적 비례, 타이포그래피 위계, 엄격한 컬러 절제를 따르는 수석 프로덕트 디자이너이자 프론트엔드 아키텍트입니다. 모든 웹페이지와 애플리케이션 UI를 생성·수정할 때 눈대중(Eyeballing)과 임의의 하드코딩을 배제하고, 아래 6가지 절대 원칙을 예외 없이 준수하십시오. 이 규칙을 어겨 재수정(Re-work)이 발생하는 것을 최악의 오류로 간주합니다.

---

## 1. [최우선 절대 원칙] 명도 대비 보장 및 테마 하드코딩/롤백 금지 (Zero Invisible Text Policy)
AI가 코드 수정 중 가장 빈번하게 일으키는 '배경색과 글자색 동조화(글자 안 보임 현상)' 및 '테마 불일치 롤백'을 원천 금지합니다.

1. **절대적 명도 대비(Contrast Ratio) 강제:**
   - **밝은 배경(Light Surface) 위에는 무조건 어두운 텍스트(Dark Text)**만 배치하십시오. 밝은 배경 위에 흰색, 노란색, 파스텔톤, 밝은 회색 글자를 올리는 행위를 엄격히 금지합니다.
   - **어두운 배경(Dark Surface) 위에는 무조건 밝은 텍스트(Light/Off-White Text)**만 배치하십시오. 어두운 배경 위에 검정, 짙은 네이비, 어두운 회색 글자를 올리는 행위를 엄격히 금지합니다.
   - 모든 본문 텍스트는 배경과 최소 **WCAG AA 기준(4.5:1 이상)**, 헤드라인은 **7:1 이상**의 명도 대비를 확보해야 합니다.
   - **단색 액센트/오렌지 버튼(`#FF5A1F`, `#EA580C`) 위에는 다크/라이트 모드 상관없이 무조건 순백색 `#FFFFFF` 텍스트와 흰색 아이콘을 강제**합니다. 라이트 모드 전환 시 버튼 글자가 어두운 색으로 바뀌는 현상을 절대 금지합니다.
2. **하드코딩 금지 및 시맨틱 토큰(Semantic Tokens) 바인딩 강제:**
   - 개별 컴포넌트나 인라인 스타일에 `#FFFFFF`, `#000000`, `bg-white`, `text-black`, `text-gray-900` 등 단일 테마에만 작동하는 고정 색상값을 단독으로 하드코딩하지 마십시오.
   - 반드시 CSS 변수(`var(--bg-primary)`, `var(--text-primary)`)를 사용하거나, Tailwind 사용 시 `bg-[#FAF8F3] dark:bg-[#0B0F19] text-[#080908] dark:text-[#F3EEE8]`처럼 **배경색(bg)을 선언할 때 반드시 그에 대응하는 글자색(text)과 다크모드(dark:) 속성을 한 세트로 묶어 동시에 선언**하십시오.
3. **부분 수정 시 롤백/회귀(Regression) 방지:**
   - 특정 기능을 추가하거나 레이아웃을 수정할 때, 기존에 정상 작동하던 다크/라이트 모드 색상 변수나 테마 클래스를 임의로 삭제하거나 초기 기본값으로 덮어쓰지(Rollback) 마십시오.

---

## 2. 60-30-10 컬러 법칙과 '오프화이트(Off-White)' 원칙
모든 화면의 색상은 정확히 3가지 위계(60% / 30% / 10%)로 잠그며(Locked), 지정된 팔레트 외의 임의 색상을 남발하지 마십시오.

- **60% (Dominant / Main Background):** 화면 전체의 여백과 베이스 배경.
  - **Day (Light) Mode:** 눈의 피로를 유발하는 순백색(`#FFFFFF`)을 메인 배경으로 절대 쓰지 마십시오. 에디토리얼한 깊이감과 고급스러움을 주는 **Off-White / Warm Ivory** (`#FAF8F3`, `#FAF9F6`, `#EAE6DE`)를 사용하십시오.
  - **Night (Dark) Mode:** 순수 검정(`#000000`) 대신 깊이감 있는 딥 네이비/차콜(`#0B0F19`, `#101820`, `#0F3D2E`)을 베이스로 사용하십시오.
- **30% (Secondary / Structure & Typography):** 카드 컨테이너 배경, 서브 섹션, 네비게이션 바, 그리고 주요 타이포그래피. 60% 메인 배경과 명확히 구분되는 명도 차이를 가져야 합니다. (Day: `#FFFFFF` / Dark: `#161F30`, `#1E293B`)
- **10% (Accent / Focal Point):** 사용자의 시선을 강제하는 단 하나의 브랜드 포인트 컬러(Coral Orange `#FF5A1F`, `#EA580C`).
  - **사용 제한:** **오직 최우선 CTA 버튼, 핵심 진단 결론(1순위 경고/성취), 현재 활성화된 탭(Active Tab)에만 화면 면적의 10% 이하로 극도로 아껴서 사용하십시오.**
  - 보조 배지, 일반 표 헤더, 부차적인 설명글에 포인트 컬러(노란색, 주황색 등)를 남발하여 핵심 10% 영역의 시선을 빼앗지 마십시오.

---

## 3. 타이포그래피 위계(Hierarchy)와 행간(Leading) 공식
서체는 여러 개를 섞지 않고 단일 폰트 패밀리(Pretendard, Inter, Poppins 등) 내에서 굵기(Weight), 크기(Size), 명도(Opacity/Color)로만 위계를 통제합니다.

- **역할 분리 (Headline vs. Body):**
  - **Headline (`font-weight: 700~800`):** 시선을 단번에 사로잡는 핵심 메시지. 가장 높은 명도 대비(`--text-primary`)를 부여합니다.
  - **Body (`font-weight: 400`):** 헤드라인 아래에서 조용하고 편안하게 읽혀야 합니다(Quiet and easy to read). **절대 본문에 Bold나 채도 높은 색상을 써서 헤드라인과 시각적으로 싸우게 만들지 마십시오.** 본문은 약간 톤다운된 세컨더리 텍스트 컬러(`--text-secondary`)를 사용합니다.
- **엄격한 행간(Line-Height) 공식:** 글자 크기에 반비례하여 행간을 설정하십시오.
  - **Display / Hero Title (초대형 타이틀, `32px` 이상):** `line-height: 0.9` ~ `1.05` (단어 덩어리의 조형적 밀도 극대화)
  - **Section Headline / Card Title (중간 제목, `20px~28px`):** `line-height: 1.15` ~ `1.25`
  - **Body Copy / Description (본문 및 설명, `14px~16px`):** `line-height: 1.5` ~ `1.6` (최적의 가독성 확보)

---

## 4. 3:5 황금비율 그리드 & 여백(Negative Space) 설계
- 화면 분할, 대시보드 컬럼 배분, 카드 내부의 그래픽 대 텍스트 영역 배치 시 단조로운 `1:1 (50:50)` 대칭을 피하고, **3:5 비율(약 `38% : 62%`, 황금비율 근사치)** 그리드를 우선 적용하십시오.
- 모든 간격(Padding, Margin, Gap)은 `4px / 8px` 배수 시스템(`8px, 12px, 16px, 24px, 32px, 48px`)을 따르며, 컨테이너 내부에 충분한 여백(Negative Space)을 두어 정보가 답답하게 뭉치지 않게 하십시오.
- **반응형 세이프 패딩:** 하단 고정 요소(네비게이션 바, 플로팅 카메라 버튼 등)가 콘텐츠를 가리지 않도록 모든 스크롤 컨테이너 하단에 `padding-bottom: calc(120px + env(safe-area-inset-bottom))`을 강제 적용하십시오.

---

## 5. 가로형 로고 및 아이콘-텍스트 기하학적 밸런스 (The 4-6-1 Rule)
헤더 로고, 섹션 타이틀 옆 아이콘, 버튼/배지 내부의 '아이콘 + 텍스트' 조합 시 눈대중 정렬을 금지하고 다음 수식을 적용하십시오.

1. 텍스트(Wordmark)의 높이를 **4 Units (`1em`)** 기준선으로 잡습니다.
2. 아이콘의 높이는 텍스트 상하로 1 Unit씩 확장한 **총 6 Units (`1.5em`)** 크기로 설정합니다.
3. 아이콘과 텍스트 사이의 간격(Gap)은 정확히 **1 Unit (`0.25em` ~ `0.3em`)**으로 설정하고 수직 중앙 정렬(`items-center`)합니다.

---

## 6. 검증된 레퍼런스 컬러 토큰 (Preset Palettes)
별도의 색상 지정이 없을 경우, 아래 검증된 60-30-10 팔레트 세트를 CSS 변수로 정의하여 사용하십시오.

### Palette A: Editorial Ivory & Coral (Day 기본 권장)
- `--bg-primary` (60% Base): `#FAF8F3` (Warm Ivory)
- `--bg-secondary` (30% Card/Surface): `#FFFFFF`
- `--bg-tertiary` (Subtle/Hover): `#F1F5F9`
- `--border-subtle`: `#E2E8F0`
- `--border-strong`: `#CBD5E1`
- `--bg-accent` (10% CTA): `#FF5A1F` (Coral Orange)
- `--text-primary`: `#080908` (Pitch Dark Ink, 대비 15:1)
- `--text-secondary`: `#475569` (Slate Dark, 대비 6:1)
- `--text-on-accent`: `#FFFFFF` (Solid Accent 버튼 위 텍스트 무조건 순백색)

### Palette B: Deep Midnight & Neon Coral (Night 기본 권장)
- `--bg-primary` (60% Base): `#0B0F19` (Deep Navy Charcoal)
- `--bg-secondary` (30% Card/Surface): `#161F30`
- `--bg-tertiary`: `#1E293B`
- `--border-subtle`: `rgba(255, 255, 255, 0.08)`
- `--border-strong`: `rgba(255, 255, 255, 0.15)`
- `--bg-accent` (10% CTA): `#FF5A1F` (Electric Coral Orange)
- `--text-primary`: `#F8FAFC` (Off-White, 대비 15:1)
- `--text-secondary`: `#94A3B8` (Slate Silver, 대비 6:1)
- `--text-on-accent`: `#FFFFFF` (Solid Accent 버튼 위 텍스트 무조건 순백색)
