# HTML의 기본 구조
📅 2024-03-11

<h2 id="0-html--css--javascript">0. HTML + CSS + JavaScript</h2>
<ul>
<li>HTML : 웹콘텐츠의 구조 표현</li>
<li>CSS : 적절한 배치와 보기좋은 디자인 표현</li>
<li>Javascript : 사용자 요청을 잘 반영하여 HTML, CSS를 이리저리 움직이고 변경. 동적인 프로그래밍.<br />
<br />
</li>
</ul>
<hr />
<h2 id="1-html의-기본-구성-요소--태그-속성-문법-주석">1. HTML의 기본 구성 요소 ; 태그, 속성, 문법, 주석</h2>
<h3 id="1-1-태그">1-1. 태그</h3>
<ul>
<li>태그의 형식 : &lt;태그명&gt;</li>
<li>웹 페이지 구성 요소를 정의하는 역할</li>
<li>HTML분법을 이루는 가장 작은 단위</li>
</ul>
<br />

<h3 id="1-2-속성">1-2. 속성</h3>
<ul>
<li><p>속성의 형식
&lt;태그명 속성명 = &quot;속성값&quot;&gt;</p>
</li>
<li><p>즉, 태그가 없이 속성을 사용할 순 없다.</p>
</li>
<li><p>태그에 어떤 의미나 기능을 보충하는 역할 속성을 사용할지 말지, 몇 개를 사용할지는 내 선택이다. 
ex.</p>
<pre><code>&lt;html&gt; // 문법의 시작
&lt;html lang = &quot;ko&quot; // 주언어가 한글로 된 HTML문서의 시작</code></pre><br />

</li>
</ul>
<h3 id="1-3-문법">1-3. 문법</h3>
<ul>
<li><p>콘텐츠가 있는 문법</p>
<pre><code>&lt;title&gt;About grammer&lt;/title&gt;</code></pre></li>
<li><p>콘텐츠가 없는 문법</p>
<pre><code>&lt;br&gt;</code></pre><p>콘텐츠가 없는 문법은 종료태그가 없이 시작태그만 사용한다.</p>
</li>
</ul>
<br />

<h3 id="1-4-주석">1-4. 주석</h3>
<ul>
<li>주석의 형식<pre><code>&lt;!-- 주석 내용 --&gt;</code></pre></li>
<li>보안상 중요한 내용을 넣으면 안됨
(왜냐면 웹브라우저의 소스보기에 주석이 다 표시되니까..)</li>
</ul>
<br />
<br />

<hr />
<h2 id="2-html의-기본구조">2. HTML의 기본구조</h2>
<p>설명을 위해 웹페이지를 하나 만들어보자.
코드는 다음과 같다.
(visual studio code에선 !를 입력하면 자동 완성 목록이 나오고,
idle에선 html파일을 새로 생성하면 자동적으로 포맷이 작성되어 있다.)</p>
<pre><code class="language-HTML">&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
&lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot;&gt;
    &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;IE=edge&quot;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
    &lt;title&gt;Document&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;p&gt;나의 첫번째 웹&lt;/p&gt;

&lt;/body&gt;
&lt;/html&gt;

&lt;코드 설명&gt;

&lt;!DOCTYPE html&gt; &lt;!--DTD(Document Typle Definition)의 약자로, '문서형 정의'를 의미함
웹브라우저가 처리할 HTML문서가 어떤 문서 형식을 따라야 할지를 알려줌
HTML문서를 작성할 때 항상 처음에 넣어야 함--&gt;

&lt;html lang=&quot;en&quot;&gt; &lt;!--주언어는 영어를 사용함
모든 태그는 html시작과 끝 태그들의 사이에 위치해야함 --&gt;

&lt;head&gt; &lt;!-- head 태그는 문서의 메타데이터를 정의함
메타데이터란 HTML의 문서에 대한 정보로, 웹 브라우저에는 직접 노출되지 않음
meta, title, link, style, script등의 태그를 사용함 --&gt;

    &lt;meta charset=&quot;UTF-8&quot;&gt; &lt;!-- 문자 코드셋은 UTF-8(이걸 주로 사용함)
    coded character set이란 의미, 파일의 정보 형태가 어떤 언어로 되어있는지. --&gt;
    &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;IE=edge&quot;&gt; &lt;!-- 최신 렌더링 엔진으로 강제지정 --&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
    &lt;!-- 기기의 화면 너비에 맞추기
    뷰포트는 웹페이지에 접속했을 때 사용자에게 보이는 화면 영역을 의미 --&gt;
    &lt;title&gt;Document&lt;/title&gt; // 문서의 제목은 title
    &lt;!-- 문서의 제목은 중복 금지
    중복될 시 검색 엔진이 해당 제목의 문서에 대한 신뢰성이 떨어진다 판단, 검색 엔진 노출시에 불이익을 줌) --&gt;
&lt;/head&gt;

&lt;body&gt; &lt;!-- body태그는 웹 브라우저에 노출되는 내용을 작성하는 영역 --&gt;
    &lt;p&gt;나의 첫번째 웹&lt;/p&gt;
&lt;/body&gt;

&lt;/html&gt;</code></pre>