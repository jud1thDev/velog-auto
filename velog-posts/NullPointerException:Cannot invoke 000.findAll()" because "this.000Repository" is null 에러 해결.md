# NullPointerException:Cannot invoke 000.findAll()" because "this.000Repository" is null 에러 해결
📅 2024-05-30

<h1 id="문제">문제</h1>
<blockquote>
<p>java.lang.NullPointerException: Cannot invoke &quot;com.efub.leadtoyproject.domain.review.repository.ReviewRepository.findAllByProduct(com.efub.leadtoyproject.domain.product.domain.Product)&quot; because &quot;this.reviewRepository&quot; is null</p>
</blockquote>
<h1 id="원인">원인</h1>
<p>reviewRepository 필드가 null인 상태에서 findAllByProduct 메서드를 호출하려고 할 때 발생한 문제이다. 이는 <strong>해당 의존성이 제대로 주입되지 않았기 때문이다.</strong></p>
<h1 id="해결">해결</h1>
<p>생성자 주입 방식을 바꾸는 과정에서 <code>final</code> 을 빼먹어서 문제가 발생했던 것이었다. </p>
<h2 id="생성자-주입-방식">생성자 주입 방식</h2>
<h3 id="기본-생성자-주입">기본 생성자 주입</h3>
<pre><code class="language-java">@Service
public class ReviewService {
    private final ReviewRepository reviewRepository;

    @Autowired
    public ReviewService(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }</code></pre>
<p>이때, <strong>클래스에 생성자가 하나만 있는 경우 <code>@Autowired</code> 를 생략해주어도</strong> 된다. 
<br /></p>
<h3 id="다중-생성자-주입">다중 생성자 주입</h3>
<pre><code class="language-java">@Service
public class ReviewService {
    private final ReviewRepository reviewRepository;
    private final ProductRepository productRepository;

    @Autowired
    public ReviewService(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
        this.reviewRepository = null; // 다른 생성자를 통한 주입이 아닌 경우
    }

    @Autowired
    public ReviewService(ReviewRepository reviewRepository, ProductRepository productRepository) {
        this.reviewRepository = reviewRepository;
        this.productRepository = productRepository;
    }

}</code></pre>
<br />

<h3 id="lombok을-사용한-생성자-주입추천">Lombok을 사용한 생성자 주입(추천)</h3>
<pre><code class="language-java">@Service
@RequiredArgsConstructor
public class ReviewService {
    private final ReviewRepository reviewRepository;
    private final ProductRepository productRepository;

}</code></pre>
<p>이때, <strong>접근자를 final로 선언해야</strong> lombok이 작동한다!!!</p>