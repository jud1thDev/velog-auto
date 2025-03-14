# Spring Boot에서 spotify API를 활용해보자 (1)
📅 2024-08-13

<p align="center">

  <img src="https://velog.velcdn.com/images/8w8u8/post/3206701a-bd8a-419f-a117-33bef9a1240c/image.png" width="300" />

<p><a href="https://github.com/EFUB4-Jukebox/songpin-backend">나의 음악지도, SongPin</a>
  <img alt="" src="https://velog.velcdn.com/images/8w8u8/post/88e56db6-92d0-4710-b151-6d83098d5690/image.png" /></p>
</p>

<hr />
<p>SongPin 프로젝트를 구현하는 과정에서, 사용자는 Pin 생성 시 함께 등록할 song을 선택해야 하는데 이때 Spotify API를 활용한 검색 기능을 구현해야했다.</p>
<p>나는 Spring Boot 3.3.1 Gradle 환경에서 진행하였다.</p>
<h2 id="1-buildgradle에-추가">1. build.gradle에 추가</h2>
<pre><code class="language-JSON">dependencies { 
        implementation 'se.michaelthelin.spotify:spotify-web-api-java:8.0.0' // 추가
}</code></pre>
<p>먼저 spotify 라이브러리 활용을 위한 의존성을 추가한다. </p>
<h2 id="2-spotify">2. Spotify</h2>
<h3 id="2-1-spotify-for-developers-참고">2-1. Spotify for Developers 참고</h3>
<p><a href="https://developer.spotify.com/documentation/web-api/tutorials/getting-started">https://developer.spotify.com/documentation/web-api/tutorials/getting-started</a>
위의 링크에서 Web API를 활용하는 순서를 확인할 수 있다. 시키는 대로 해주면 된다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/d995037e-7df6-40fc-971e-0758f7c1e86b/image.png" /></p>
<h3 id="2-2-회원가입">2-2. 회원가입</h3>
<p>스포티파이에 회원가입이 되어있지 않다면, 먼저 회원가입을 해준다.</p>
<h3 id="2-3-create-app">2-3. Create App</h3>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/6c947c68-567f-4e29-bd3c-e747bff0b3c6/image.png" />
Create app 클릭</p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/aa750106-2442-46a4-9bb7-64c3242de683/image.png" />
적절하게 채워주고, Save.</p>
<p>스포티계정을 만들고 난 <strong>직후</strong> Create App을 하려고 하면 </p>
<blockquote>
<p>Your account is not ready, please wait a few minutes and try again. </p>
</blockquote>
<p>에러가 뜰 수 있다. 한 시간 뒤 다시 해보니 성공적으로 Create 할 수 있었다. </p>
<h3 id="2-4-access-token-요청">2-4. Access Token 요청</h3>
<p><a href="https://developer.spotify.com/dashboard">Dashboard</a>로 이동해서, 방금 만든 App의 이름을 클릭하고, Settings 버튼을 클릭한다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7898299b-7049-48a0-84a4-4854b188ea5e/image.png" />
Client ID, Client secret을 확인한다.</p>
<h2 id="3-applicationyml에-추가">3. Application.yml에 추가</h2>
<pre><code class="language-YAML">spotify:
  client-id: #
  client-secret: #</code></pre>
<p>#부분에 위에서 확인한 Client ID, Client secret를 적절하게 넣어준다. </p>
<hr />
<p>참고
<a href="https://github.com/spotify-web-api-java/spotify-web-api-java">https://github.com/spotify-web-api-java/spotify-web-api-java</a></p>