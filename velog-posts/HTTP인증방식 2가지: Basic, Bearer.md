# HTTP인증방식 2가지: Basic, Bearer
📅 2024-05-30

<h1 id="http인증-이해하기-basic과-bearer-인증">HTTP인증 이해하기: Basic과 Bearer 인증</h1>
<h2 id="http-통신과-인증의-필요성">HTTP 통신과 인증의 필요성</h2>
<p>HTTP 통신은 웹 페이지와 리소스를 불러오기 위해 클라이언트(보통 웹 브라우저)와 서버 간의 요청(Request)과 응답(Response)으로 이루어진다.
내가 지금 하고 있는 프로젝트에서, 리뷰 수정 및 삭제에 관한 권한은 작성자에게 있어야한다. 즉, <strong>서버는 해당 클라이언트가 요청한 리소스에 접근할 권한이 있는지 확인해야</strong> 한다.</p>
<br />

<h2 id="http-인증-헤더">HTTP 인증 헤더</h2>
<p>HTTP 인증 프레임워크는 RFC 7235에 정의되어 있으며, 요청 시 <strong>인증 헤더를 사용</strong>한다. 인증 헤더의 형식은 다음과 같다:</p>
<pre><code class="language-php">Authorization: &lt;type&gt; &lt;credentials&gt;</code></pre>
<ul>
<li>success response :  <code>200 OK</code> </li>
<li>failure response : <ul>
<li>인증 헤더 누락 : <code>403 Forbidden</code></li>
<li>권한 없음 : <code>401 Unauthorized</code> <br />

</li>
</ul>
</li>
</ul>
<h2 id="대표적인-인증-방식-2가지">대표적인 인증 방식 2가지</h2>
<h3 id="basic-인증-방식">Basic 인증 방식</h3>
<p>Basic 인증은 가장 기본적인 인증 방식이다. 사용자 ID와 비밀번호를 사용하며, 이를 <strong>&quot;사용자ID:비밀번호&quot;</strong> 형식의 문자열로 만들어 <strong>Base64</strong>로 인코딩하여 전송한다. </p>
<pre><code class="language-bash">Authorization: Basic base64({USERNAME}:{PASSWORD})</code></pre>
<ul>
<li>장점 : <ul>
<li>사용자 ID와 비밀번호만으로 인증 가능하다.</li>
<li>그렇기에, 간단하고 구현이 쉽다. </li>
</ul>
</li>
<li>단점:<ul>
<li>Base64 인코딩은 쉽게 복호화 가능하여 보안에 취약하다.</li>
<li>반드시 HTTPS를 사용해야 안전하다.</li>
<li>사용자 수가 많아지면 서버 부담이 증가한다.</li>
<li>세부적인 권한 제어가 어렵다.</li>
</ul>
</li>
</ul>
<h3 id="bearer-인증-방식">Bearer 인증 방식</h3>
<p>Bearer 인증은 <strong>OAuth 2.0 프레임워크</strong>에서 사용하는 토큰 기반 인증 방식이다. &quot;Bearer&quot;는 &quot;이 토큰의 소유자에게 권한을 부여하라&quot;는 의미다. Bearer 토큰을 인증 헤더에 입력하여 전송한다:</p>
<pre><code class="language-makefile">Authorization: Bearer &lt;token&gt;</code></pre>
<ul>
<li>장점:<ul>
<li>안전하고 확장성이 높다.</li>
<li>Bearer 토큰은 쉽게 복호화할 수 없으며, OAuth 프레임워크는 SSL/TLS를 필수로 사용한다.
서버에서 토큰의 리소스 접근 권한을 쉽게 철회할 수 있고, 유효기간을 설정할 수 있다.</li>
<li>여러 서비스 및 서버 간에 토큰을 공유할 수 있다.</li>
</ul>
</li>
<li>단점:<ul>
<li>Bearer 토큰이 외부에 노출되면 문제가 생길 수 있다. (하지만 보안 장치를 잘 구축하면 위험을 줄일 수 있다.)</li>
</ul>
</li>
</ul>
<br /> 

<h1 id="oauth-20-프레임워크">OAuth 2.0 프레임워크</h1>
<p>OAuth 2.0 프레임워크는 다양한 서비스 간에 안전하게 데이터를 전송하기 위해 고안되었다. 주요 구성 요소는 다음과 같다:</p>
<ul>
<li>리소스 소유자: 사용자</li>
<li>클라이언트: 사용자의 정보를 접근하는 제3자 서비스</li>
<li>인증 서버: 클라이언트의 접근을 관리</li>
<li>리소스 서버: 보호된 데이터를 관리</li>
</ul>
<p>사용자가 동의하면 인증 서버는 클라이언트에게 액세스 토큰을 발급하고, 클라이언트는 이를 사용해 리소스 서버에 접근한다.</p>
<h1 id="json-web-token-jwt">JSON Web Token (JWT)</h1>
<p>JWT는 Bearer 토큰의 한 형태로, <strong>클라이언트와 서버 간에 정보를 안전하게 전송하기 위해</strong> 사용된다. </p>
<p>JWT는 인코딩된 JSON 객체로,
세 부분으로 구성된다:</p>
<ul>
<li>Header: 토큰의 타입과 해싱 알고리즘 정보를 포함한다.</li>
<li>Payload: 토큰에 담을 claim을 포함하며, 사용자 정보와 추가 데이터가 들어간다.</li>
<li>Signature: 앞의 두 부분을 합쳐서 비밀 키로 암호화한 것으로, <strong>해당 토큰이 변조되지 않았음을 확인</strong>한다.</li>
</ul>
<hr />
<ul>
<li>참고
<a href="https://velog.io/@tosspayments/Basic-%EC%9D%B8%EC%A6%9D%EA%B3%BC-Bearer-%EC%9D%B8%EC%A6%9D%EC%9D%98-%EB%AA%A8%EB%93%A0-%EA%B2%83">https://velog.io/@tosspayments/Basic-%EC%9D%B8%EC%A6%9D%EA%B3%BC-Bearer-%EC%9D%B8%EC%A6%9D%EC%9D%98-%EB%AA%A8%EB%93%A0-%EA%B2%83</a>
<a href="https://suddiyo.tistory.com/entry/Spring-JWTJson-Web-Token%EB%9E%80-%EA%B5%AC%EC%A1%B0-%EC%95%94%ED%98%B8%ED%99%94-%EB%B0%A9%EB%B2%95-%EC%9E%A5%EB%8B%A8%EC%A0%90">https://suddiyo.tistory.com/entry/Spring-JWTJson-Web-Token%EB%9E%80-%EA%B5%AC%EC%A1%B0-%EC%95%94%ED%98%B8%ED%99%94-%EB%B0%A9%EB%B2%95-%EC%9E%A5%EB%8B%A8%EC%A0%90</a></li>
</ul>