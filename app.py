{% extends "base.html" %}
{% block title %}Sharifi Exchange | صرافی شریفی{% endblock %}

{% block content %}

<style>
.sharifi-home {
  --navy:#061d38;
  --blue:#0b4773;
  --gold:#edbd55;
  --green:#0ba66b;
  color:#142d49;
  font-family:inherit;
}
.sharifi-home * {box-sizing:border-box}
.sharifi-home .wrap {width:min(1250px,100%);margin:auto;padding:0 10px}
.sharifi-home .hero {
  position:relative;
  display:grid;
  grid-template-columns:1fr 1fr;
  align-items:center;
  gap:25px;
  min-height:390px;
  padding:38px;
  overflow:hidden;
  border-radius:20px;
  color:white;
  background:
    radial-gradient(ellipse at 78% 55%,#17618a 0%,transparent 43%),
    linear-gradient(120deg,#04172e,#073b67 70%,#082a4b);
}
.sharifi-home .hero:before {
  content:"";
  position:absolute;inset:0;
  opacity:.13;
  background-image:radial-gradient(#fff 1px,transparent 1px);
  background-size:23px 23px;
  pointer-events:none;
}
.sharifi-home .hero-copy,.sharifi-home .money-scene {
  position:relative;z-index:1;
}
.sharifi-home .eyebrow {color:var(--gold);font-weight:800;font-size:14px}
.sharifi-home h1 {
  font-size:clamp(29px,4vw,46px);
  line-height:1.5;margin:13px 0;
  color:white;font-weight:900;
}
.sharifi-home h1 span {color:var(--gold)}
.sharifi-home .hero-copy p {line-height:2.1;color:#e4edf6;font-size:15px}
.sharifi-home .actions {display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.sharifi-home .btn {
  display:inline-flex;justify-content:center;align-items:center;
  gap:8px;padding:13px 22px;border-radius:30px;
  text-decoration:none;font-weight:800;transition:.2s;
}
.sharifi-home .btn:hover {transform:translateY(-3px)}
.sharifi-home .gold-btn {background:linear-gradient(120deg,#ffe49a,#dca638);color:#102b49}
.sharifi-home .line-btn {border:1px solid var(--gold);color:white}
.sharifi-home .trust {display:flex;gap:15px;flex-wrap:wrap;margin-top:22px;font-size:12px;color:#e5edf7}
.sharifi-home .money-scene {
  min-height:270px;display:flex;align-items:center;justify-content:center;
}
.sharifi-home .globe {
  width:175px;height:175px;border-radius:50%;
  display:grid;place-items:center;
  font-size:100px;
  background:radial-gradient(circle at 35% 30%,#fff,#b9d7e7 40%,#23658c 75%);
  box-shadow:0 0 50px #58a6d6,0 20px 35px #00152b;
}
.sharifi-home .note {
  position:absolute;width:190px;height:100px;
  border:2px solid rgba(255,255,255,.7);
  border-radius:8px;display:flex;
  flex-direction:column;justify-content:space-between;
  padding:12px;color:#163c40;font-weight:900;
  box-shadow:0 12px 25px #00152b99;
}
.sharifi-home .note small {font-size:10px}
.sharifi-home .note strong {font-size:27px}
.sharifi-home .note-usd {
  top:12px;right:5px;transform:rotate(-13deg);
  background:linear-gradient(135deg,#e8f1d9,#7eaa8c);
}
.sharifi-home .note-afn {
  bottom:15px;left:0;transform:rotate(9deg);
  background:linear-gradient(135deg,#f5e5b7,#c69c54);
}
.sharifi-home .note-eur {
  bottom:0;right:12px;transform:rotate(-5deg);
  background:linear-gradient(135deg,#d6e8f6,#81a9d1);
}
.sharifi-home .section-head {
  display:flex;justify-content:space-between;align-items:center;
  gap:12px;margin:28px 0 14px;
}
.sharifi-home .section-head h2 {font-size:21px;margin:0;color:var(--navy)}
.sharifi-home .section-head a {color:#ad7d22;text-decoration:none;font-weight:800;font-size:13px}
.sharifi-home .main-grid {display:grid;grid-template-columns:1.15fr .85fr;gap:18px}
.sharifi-home .panel {
  background:white;border:1px solid #e0e8f0;
  border-radius:15px;overflow:hidden;
  box-shadow:0 6px 22px #102b4910;
}
.sharifi-home .panel-title {
  background:linear-gradient(100deg,#061e39,#0b4773);
  color:white;padding:16px 19px;font-weight:900;
  display:flex;justify-content:space-between;align-items:center;
}
.sharifi-home .live-dot {
  width:8px;height:8px;background:#2de18c;
  display:inline-block;border-radius:50%;margin-left:6px;
  box-shadow:0 0 9px #2de18c;
}
.sharifi-home .table-scroll {overflow-x:auto}
.sharifi-home table {width:100%;border-collapse:collapse;text-align:center;font-size:13px}
.sharifi-home th {background:#edf3f9;padding:13px 8px;color:#173653;white-space:nowrap}
.sharifi-home td {padding:12px 8px;border-bottom:1px solid #edf0f4}
.sharifi-home tbody tr:hover {background:#f5f9ff}
.sharifi-home .currency-name {text-align:right;font-weight:700;white-space:nowrap}
.sharifi-home .code {background:#edf3fa;padding:4px 8px;border-radius:5px;font-weight:800}
.sharifi-home .buy {color:#159447;font-weight:900}
.sharifi-home .sell {color:#c54a4a;font-weight:900}
.sharifi-home .muted {color:#8794a2;font-size:11px}
.sharifi-home .panel-foot {padding:12px 16px;color:#77879a;font-size:11px}
.sharifi-home .converter {padding:20px;background:linear-gradient(145deg,#f4f9ff,#fff)}
.sharifi-home .converter label {display:block;font-size:13px;font-weight:800;margin-bottom:8px}
.sharifi-home .converter select,
.sharifi-home .converter input {
  width:100%;padding:13px;border:1px solid #d9e3ee;
  border-radius:9px;background:white;color:#132f4d;
  font:inherit;font-size:15px;outline:none;
}
.sharifi-home .converter select:focus,
.sharifi-home .converter input:focus {border-color:#2e83bd}
.sharifi-home .convert-grid {display:grid;grid-template-columns:1fr 1fr;gap:12px}
.sharifi-home .swap {
  display:flex;justify-content:center;align-items:center;
  width:38px;height:38px;margin:12px auto;
  border-radius:50%;background:#092c4d;color:white;
  border:0;font-size:20px;cursor:pointer;
}
.sharifi-home .result {
  background:#eaf8f1;border:1px solid #c6ebd7;
  padding:16px;border-radius:10px;margin-top:14px;
}
.sharifi-home .result strong {font-size:25px;color:#07844f}
.sharifi-home .convert-btn {
  display:block;width:100%;padding:14px;border:0;
  border-radius:9px;background:linear-gradient(100deg,#10b875,#078a54);
  color:white;font-weight:900;font-size:15px;cursor:pointer;margin-top:14px;
}
.sharifi-home .services {
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:13px;margin:18px 0 28px;
}
.sharifi-home .service {
  text-align:center;padding:22px 12px;background:white;
  border:1px solid #e3ebf3;border-radius:14px;
  box-shadow:0 5px 18px #102b4909;transition:.2s;
}
.sharifi-home .service:hover {transform:translateY(-4px);border-color:#e3b94d}
.sharifi-home .service-icon {
  width:54px;height:54px;border-radius:50%;
  background:#eaf4ff;display:grid;place-items:center;
  margin:auto auto 12px;font-size:25px;
}
.sharifi-home .service h3 {font-size:14px;margin:8px 0}
.sharifi-home .service p {font-size:11px;line-height:1.9;color:#77879a}
.sharifi-home .service a {color:#a87820;text-decoration:none;font-weight:800;font-size:12px}
.sharifi-home .why {
  padding:22px;border-radius:14px;
  background:linear-gradient(110deg,#edf5fc,#fff9e9);
  display:grid;grid-template-columns:1fr 1fr;gap:15px;
  margin-bottom:25px;
}
.sharifi-home .why h2 {margin:0 0 12px;font-size:19px}
.sharifi-home .why-list {display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:13px}
.sharifi-home .why-list span:before {content:"✓";color:#0ca45d;font-weight:900;margin-left:7px}
.sharifi-home .source-note {font-size:11px;color:#748398;line-height:1.9}
.sharifi-home .lang-btn {
  border:1px solid #d8e3ef;background:#fff;color:#173653;
  padding:8px 13px;border-radius:20px;cursor:pointer;font-weight:800;
}
@media(max-width:850px) {
  .sharifi-home .hero {grid-template-columns:1fr;text-align:center;padding:30px 20px}
  .sharifi-home .actions,.sharifi-home .trust {justify-content:center}
  .sharifi-home .main-grid {grid-template-columns:1fr}
  .sharifi-home .services {grid-template-columns:repeat(2,1fr)}
}
@media(max-width:480px) {
  .sharifi-home .hero {padding:27px 14px}
  .sharifi-home .money-scene {min-height:230px;transform:scale(.85)}
  .sharifi-home .services {gap:8px}
  .sharifi-home .service {padding:15px 7px}
  .sharifi-home .why {grid-template-columns:1fr}
  .sharifi-home .why-list {grid-template-columns:1fr 1fr}
  .sharifi-home table {font-size:11px}
  .sharifi-home th,.sharifi-home td {padding:9px 5px}
}
</style>

<div class="sharifi-home" id="sharifiHome">
<div class="wrap">

  <div class="section-head" style="margin-top:8px">
    <div>
      <strong data-fa="صرافی شریفی" data-en="SHARIFI EXCHANGE">صرافی شریفی</strong>
      <div class="muted" data-fa="همراه مطمئن شما در تبادلات اسعار" data-en="Your trusted currency exchange partner">همراه مطمئن شما در تبادلات اسعار</div>
    </div>
    <button class="lang-btn" id="languageToggle" type="button">🇬🇧 English</button>
  </div>

  <section class="hero">
    <div class="hero-copy">
      <span class="eyebrow" data-fa="خدمات اسعار · سمنگان، آیبیک" data-en="CURRENCY SERVICES · AYBAK, SAMANGAN">خدمات اسعار · سمنگان، آیبیک</span>
      <h1 data-fa="شریک مطمئن شما در <span>تبادلات جهانی اسعار</span>" data-en="Your Trusted Partner for <span>Global Currency Exchange</span>">
        شریک مطمئن شما در <span>تبادلات جهانی اسعار</span>
      </h1>
      <p data-fa="با صرافی شریفی، نرخ اسعار را بررسی کنید، ارزهای مختلف را محاسبه نمایید و با اطمینان درخواست تبادله خود را ثبت کنید."
         data-en="Check exchange rates, calculate different currencies, and submit your exchange request with confidence at Sharifi Exchange.">
        با صرافی شریفی، نرخ اسعار را بررسی کنید، ارزهای مختلف را محاسبه نمایید و با اطمینان درخواست تبادله خود را ثبت کنید.
      </p>
      <div class="actions">
        <a class="btn gold-btn" href="{{ url_for('convert') }}" data-fa="⇄ تبدیل اسعار" data-en="⇄ Convert Currency">⇄ تبدیل اسعار</a>
        <a class="btn line-btn" href="{{ url_for('rates_page') }}" data-fa="📊 مشاهده نرخ اسعار" data-en="📊 View Exchange Rates">📊 مشاهده نرخ اسعار</a>
      </div>
      <div class="trust">
        <span data-fa="✓ شفافیت در معاملات" data-en="✓ Transparent Transactions">✓ شفافیت در معاملات</span>
        <span data-fa="✓ خدمات مطمئن" data-en="✓ Reliable Services">✓ خدمات مطمئن</span>
        <span data-fa="✓ پشتیبانی مشتریان" data-en="✓ Customer Support">✓ پشتیبانی مشتریان</span>
      </div>
    </div>

    <div class="money-scene" aria-label="Currency notes illustration">
      <div class="globe">🌍</div>
      <div class="note note-usd"><small>UNITED STATES DOLLAR</small><strong>$100</strong><small>USD · UNITED STATES</small></div>
      <div class="note note-afn"><small>AFGHANISTAN</small><strong>؋1000</strong><small>AFGHANI · AFN</small></div>
      <div class="note note-eur"><small>EURO CURRENCY</small><strong>€100</strong><small>EURO · EUR</small></div>
    </div>
  </section>

  <div class="section-head">
    <h2 data-fa="📊 نرخ زنده اسعار" data-en="📊 Live Exchange Rates">📊 نرخ زنده اسعار</h2>
    <a href="{{ url_for('rates_page') }}" data-fa="تمام نرخ‌ها ←" data-en="All Rates →">تمام نرخ‌ها ←</a>
  </div>

  <div class="main-grid">
    <section class="panel">
      <div class="panel-title">
        <span><i class="live-dot"></i><span data-fa="نرخ خرید و فروش" data-en="Buy & Sell Rates">نرخ خرید و فروش</span></span>
        <span style="font-size:11px" data-fa="AFN" data-en="AFN">AFN</span>
      </div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th data-fa="ارز" data-en="Currency">ارز</th>
              <th data-fa="کد" data-en="Code">کد</th>
              <th data-fa="نرخ خرید" data-en="Buy Rate">نرخ خرید</th>
              <th data-fa="نرخ فروش" data-en="Sell Rate">نرخ فروش</th>
            </tr>
          </thead>
          <tbody>
          {% for r in rates if r.code != 'AFN' %}
            <tr>
              <td class="currency-name">
                <span data-fa="{{ r.name_dari }}" data-en="{{ r.name_en }}">{{ r.name_dari }}</span>
              </td>
              <td><span class="code">{{ r.code }}</span></td>
              <td class="buy">{{ r.buy_rate|money if r.buy_rate else '—' }}</td>
              <td class="sell">{{ r.sell_rate|money if r.sell_rate else '—' }}</td>
            </tr>
          {% else %}
            <tr><td colspan="4" data-fa="هنوز نرخ اسعار ثبت نشده است." data-en="No exchange rates have been entered yet.">هنوز نرخ اسعار ثبت نشده است.</td></tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
      <div class="panel-foot" data-fa="نرخ‌ها بر اساس معلومات ثبت‌شده در سیستم نمایش داده می‌شوند. برای نرخ نهایی با صرافی تماس بگیرید."
           data-en="Rates are displayed from the information stored in the system. Contact the exchange for a final quote.">
        نرخ‌ها بر اساس معلومات ثبت‌شده در سیستم نمایش داده می‌شوند. برای نرخ نهایی با صرافی تماس بگیرید.
      </div>
    </section>

    <section class="panel">
      <div class="panel-title">
        <span>⇄ <span data-fa="تبدیل اسعار" data-en="Currency Converter">تبدیل اسعار</span></span>
        <span>💱</span>
      </div>
      <div class="converter">
        <div class="convert-grid">
          <div>
            <label data-fa="از ارز" data-en="From Currency">از ارز</label>
            <select id="fromCurrency">
              {% for r in rates if r.code != 'AFN' %}
              <option value="{{ r.code }}">{{ r.code }} - {{ r.name_dari }}</option>
              {% endfor %}
            </select>
          </div>
          <div>
            <label data-fa="به ارز" data-en="To Currency">به ارز</label>
            <select id="toCurrency">
              <option value="AFN">AFN - افغانی</option>
              {% for r in rates if r.code != 'AFN' %}
              <option value="{{ r.code }}">{{ r.code }} - {{ r.name_dari }}</option>
              {% endfor %}
            </select>
          </div>
        </div>
        <button class="swap" id="swapCurrencies" type="button" aria-label="Swap currencies">⇄</button>
        <label for="amount" data-fa="مبلغ مورد نظر" data-en="Amount">مبلغ مورد نظر</label>
        <input id="amount" type="number" min="0" step="any" value="100" placeholder="100">
        <div class="result">
          <div class="muted" data-fa="مبلغ محاسبه‌شده" data-en="Converted Amount">مبلغ محاسبه‌شده</div>
          <strong id="convertedAmount">—</strong>
          <div class="muted" id="rateMessage" style="margin-top:8px" data-fa="برای محاسبه، نرخ معتبر لازم است." data-en="A valid rate is required for conversion.">برای محاسبه، نرخ معتبر لازم است.</div>
        </div>
        <button class="convert-btn" id="calculateBtn" type="button" data-fa="محاسبه اسعار ⇄" data-en="Convert Currency ⇄">محاسبه اسعار ⇄</button>
        <a href="{{ url_for('convert') }}" style="display:block;text-align:center;margin-top:13px;color:#a87820;text-decoration:none;font-weight:800;font-size:13px"
           data-fa="محاسبه‌گر پیشرفته ←" data-en="Advanced Converter →">محاسبه‌گر پیشرفته ←</a>
      </div>
    </section>
  </div>

  <div class="section-head">
    <h2 data-fa="خدمات ما" data-en="Our Services">خدمات ما</h2>
    <a href="{{ url_for('contact') }}" data-fa="تماس با ما ←" data-en="Contact Us →">تماس با ما ←</a>
  </div>

  <section class="services">
    <article class="service">
      <div class="service-icon">💱</div>
      <h3 data-fa="تبادله اسعار" data-en="Currency Exchange">تبادله اسعار</h3>
      <p data-fa="خرید و فروش ارزهای مختلف با نرخ‌های ثبت‌شده." data-en="Buy and sell different currencies at listed rates.">خرید و فروش ارزهای مختلف با نرخ‌های ثبت‌شده.</p>
      <a href="{{ url_for('new_request') }}" data-fa="ثبت درخواست ←" data-en="Submit Request →">ثبت درخواست ←</a>
    </article>
    <article class="service">
      <div class="service-icon">🌐</div>
      <h3 data-fa="انتقال بین‌المللی" data-en="International Transfer">انتقال بین‌المللی</h3>
      <p data-fa="ثبت درخواست خدمات انتقال پول و پیگیری آن." data-en="Submit and track money transfer requests.">ثبت درخواست خدمات انتقال پول و پیگیری آن.</p>
      <a href="{{ url_for('new_request') }}" data-fa="ثبت درخواست ←" data-en="Submit Request →">ثبت درخواست ←</a>
    </article>
    <article class="service">
      <div class="service-icon">🏦</div>
      <h3 data-fa="انتقال داخلی" data-en="Domestic Transfer">انتقال داخلی</h3>
      <p data-fa="ثبت درخواست خدمات انتقال داخلی." data-en="Submit domestic transfer requests.">ثبت درخواست خدمات انتقال داخلی.</p>
      <a href="{{ url_for('new_request') }}" data-fa="معلومات بیشتر ←" data-en="Learn More →">معلومات بیشتر ←</a>
    </article>
    <article class="service">
      <div class="service-icon">💵</div>
      <h3 data-fa="محاسبه اسعار" data-en="Currency Calculator">محاسبه اسعار</h3>
      <p data-fa="محاسبه مبلغ و مشاهده نرخ‌های ثبت‌شده." data-en="Calculate amounts using listed exchange rates.">محاسبه مبلغ و مشاهده نرخ‌های ثبت‌شده.</p>
      <a href="{{ url_for('convert') }}" data-fa="محاسبه کنید ←" data-en="Calculate →">محاسبه کنید ←</a>
    </article>
    <article class="service">
      <div class="service-icon">👤</div>
      <h3 data-fa="حساب مشتری" data-en="Customer Account">حساب مشتری</h3>
      <p data-fa="ثبت‌نام و پیگیری درخواست‌های خود." data-en="Register and track your requests.">ثبت‌نام و پیگیری درخواست‌های خود.</p>
      <a href="{{ url_for('register') }}" data-fa="ساخت حساب ←" data-en="Create Account →">ساخت حساب ←</a>
    </article>
    <article class="service">
      <div class="service-icon">🎧</div>
      <h3 data-fa="پشتیبانی مشتریان" data-en="Customer Support">پشتیبانی مشتریان</h3>
      <p data-fa="ارسال پرسش و دریافت راهنمایی." data-en="Ask questions and get assistance.">ارسال پرسش و دریافت راهنمایی.</p>
      <a href="{{ url_for('support') }}" data-fa="پشتیبانی ←" data-en="Support →">پشتیبانی ←</a>
    </article>
    <article class="service">
      <div class="service-icon">📈</div>
      <h3 data-fa="معلومات نرخ اسعار" data-en="Rate Information">معلومات نرخ اسعار</h3>
      <p data-fa="مشاهده نرخ‌های ثبت‌شده و تغییرات آن‌ها." data-en="View listed rates and their changes.">مشاهده نرخ‌های ثبت‌شده و تغییرات آن‌ها.</p>
      <a href="{{ url_for('rates_page') }}" data-fa="مشاهده نرخ‌ها ←" data-en="View Rates →">مشاهده نرخ‌ها ←</a>
    </article>
    <article class="service">
      <div class="service-icon">🧾</div>
      <h3 data-fa="رسید معاملات" data-en="Transaction Receipts">رسید معاملات</h3>
      <p data-fa="پیگیری رسید و معلومات درخواست‌های ثبت‌شده." data-en="Track receipts and submitted requests.">پیگیری رسید و معلومات درخواست‌های ثبت‌شده.</p>
      <a href="{{ url_for('login') }}" data-fa="ورود به حساب ←" data-en="Sign In →">ورود به حساب ←</a>
    </article>
  </section>

  <section class="why">
    <div>
      <h2 data-fa="چرا صرافی شریفی؟" data-en="Why Choose Sharifi?">چرا صرافی شریفی؟</h2>
      <p data-fa="اعتماد، شفافیت و پشتیبانی مشتریان اصول اساسی خدمات ما است."
         data-en="Trust, transparency and customer support are the foundation of our service.">
        اعتماد، شفافیت و پشتیبانی مشتریان اصول اساسی خدمات ما است.
      </p>
    </div>
    <div class="why-list">
      <span data-fa="شفافیت و صداقت" data-en="Transparency & Honesty">شفافیت و صداقت</span>
      <span data-fa="پشتیبانی حرفه‌ای" data-en="Professional Support">پشتیبانی حرفه‌ای</span>
      <span data-fa="نرخ‌های رقابتی" data-en="Competitive Rates">نرخ‌های رقابتی</span>
      <span data-fa="خدمات سریع" data-en="Fast Service">خدمات سریع</span>
      <span data-fa="معاملات امن" data-en="Secure Transactions">معاملات امن</span>
      <span data-fa="رضایت مشتری" data-en="Customer Satisfaction">رضایت مشتری</span>
    </div>
  </section>

  <p class="source-note" data-fa="یادآوری: نرخ‌های این صفحه از دیتابیس فعلی سایت خوانده می‌شوند. تا زمانی که اتصال منبع معتبر نرخ اسعار پیاده‌سازی و تأیید نشده باشد، این نرخ‌ها را نرخ لحظه‌ای بازار تلقی نکنید."
     data-en="Note: Rates on this page are read from the website's current database. Do not treat them as live market rates until a verified exchange-rate provider is connected.">
    یادآوری: نرخ‌های این صفحه از دیتابیس فعلی سایت خوانده می‌شوند. تا زمانی که اتصال منبع معتبر نرخ اسعار پیاده‌سازی و تأیید نشده باشد، این نرخ‌ها را نرخ لحظه‌ای بازار تلقی نکنید.
  </p>

</div>
</div>

<script>
(function () {
  const root = document.getElementById("sharifiHome");
  if (!root) return;

  const rates = [
    {% for r in rates if r.code != 'AFN' %}
    {
      code: {{ r.code|tojson }},
      buy: {{ (r.buy_rate or '')|tojson }},
      sell: {{ (r.sell_rate or '')|tojson }}
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ];

  let language = "fa";
  const languageButton = document.getElementById("languageToggle");

  function setLanguage(lang) {
    language = lang;
    document.documentElement.lang = lang === "fa" ? "fa" : "en";
    document.documentElement.dir = lang === "fa" ? "rtl" : "ltr";
    root.querySelectorAll("[data-fa][data-en]").forEach(el => {
      el.innerHTML = el.dataset[lang];
    });
    languageButton.textContent = lang === "fa" ? "🇬🇧 English" : "🇦🇫 دری";
    calculate();
  }

  languageButton.addEventListener("click", () => {
    setLanguage(language === "fa" ? "en" : "fa");
  });

  const from = document.getElementById("fromCurrency");
  const to = document.getElementById("toCurrency");
  const amount = document.getElementById("amount");
  const output = document.getElementById("convertedAmount");
  const message = document.getElementById("rateMessage");

  function getRate(code, side) {
    const item = rates.find(r => r.code === code);
    if (!item) return null;
    const value = Number(side === "buy" ? item.buy : item.sell);
    return Number.isFinite(value) && value > 0 ? value : null;
  }

  function calculate() {
    const value = Number(amount.value);
    const fromCode = from.value;
    const toCode = to.value;

    if (!Number.isFinite(value) || value <= 0) {
      output.textContent = "—";
      message.textContent = language === "fa" ? "مبلغ معتبر وارد کنید." : "Enter a valid amount.";
      return;
    }

    if (fromCode === toCode) {
      output.textContent = value.toLocaleString(undefined,{maximumFractionDigits:2}) + " " + toCode;
      message.textContent = language === "fa" ? "هر دو ارز یکسان هستند." : "Both currencies are the same.";
      return;
    }

    let result;
    let rateText;

    if (toCode === "AFN") {
      const rate = getRate(fromCode, "sell");
      if (!rate) return unavailable();
      result = value * rate;
      rateText = "1 " + fromCode + " = " + rate.toLocaleString() + " AFN";
    } else if (fromCode === "AFN") {
      const rate = getRate(toCode, "buy");
      if (!rate) return unavailable();
      result = value / rate;
      rateText = "1 " + toCode + " = " + rate.toLocaleString() + " AFN";
    } else {
      const sourceRate = getRate(fromCode, "sell");
      const targetRate = getRate(toCode, "buy");
      if (!sourceRate || !targetRate) return unavailable();
      result = value * sourceRate / targetRate;
      rateText = "1 " + fromCode + " ≈ " + (sourceRate / targetRate).toFixed(4) + " " + toCode;
    }

    output.textContent = result.toLocaleString(undefined,{maximumFractionDigits:2}) + " " + toCode;
    message.textContent = rateText;
  }

  function unavailable() {
    output.textContent = "—";
    message.textContent = language === "fa"
      ? "نرخ این ارز هنوز در سیستم ثبت نشده است."
      : "The exchange rate for this currency is not configured.";
  }

  document.getElementById("calculateBtn").addEventListener("click", calculate);
  amount.addEventListener("input", calculate);
  from.addEventListener("change", calculate);
  to.addEventListener("change", calculate);

  document.getElementById("swapCurrencies").addEventListener("click", () => {
    const oldFrom = from.value;
    from.value = to.value;
    to.value = oldFrom;
    calculate();
  });

  calculate();
})();
</script>

{% endblock %}
]

def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000).hex()
    return f"{salt}${digest}"

def verify_password(password, encoded):
    try:
        salt, expected = encoded.split("$", 1)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, AttributeError):
        return False

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE COLLATE NOCASE,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL DEFAULT 'customer',
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS rates (
      code TEXT PRIMARY KEY,
      name_dari TEXT NOT NULL,
      name_en TEXT NOT NULL,
      buy_rate TEXT,
      sell_rate TEXT,
      updated_at TEXT,
      updated_by INTEGER,
      source TEXT NOT NULL DEFAULT 'Not configured',
      FOREIGN KEY(updated_by) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS rate_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      code TEXT NOT NULL,
      buy_rate TEXT,
      sell_rate TEXT,
      source TEXT NOT NULL,
      changed_at TEXT NOT NULL,
      changed_by INTEGER,
      FOREIGN KEY(code) REFERENCES rates(code),
      FOREIGN KEY(changed_by) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS requests (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      request_no TEXT NOT NULL UNIQUE,
      user_id INTEGER NOT NULL,
      direction TEXT NOT NULL CHECK(direction IN ('BUY','SELL')),
      currency TEXT NOT NULL,
      amount TEXT NOT NULL,
      rate TEXT NOT NULL,
      fee TEXT NOT NULL DEFAULT '0',
      total_afn TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'Submitted',
      customer_note TEXT DEFAULT '',
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(currency) REFERENCES rates(code)
    );
    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      transaction_no TEXT NOT NULL UNIQUE,
      receipt_no TEXT NOT NULL UNIQUE,
      request_id INTEGER,
      user_id INTEGER,
      direction TEXT NOT NULL,
      currency TEXT NOT NULL,
      amount TEXT NOT NULL,
      rate TEXT NOT NULL,
      fee TEXT NOT NULL,
      total_afn TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'Completed',
      staff_id INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      note TEXT DEFAULT '',
      FOREIGN KEY(request_id) REFERENCES requests(id),
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(currency) REFERENCES rates(code),
      FOREIGN KEY(staff_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS conversations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      conversation_id INTEGER NOT NULL,
      sender_id INTEGER NOT NULL,
      body TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(conversation_id) REFERENCES conversations(id),
      FOREIGN KEY(sender_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS tickets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_no TEXT NOT NULL UNIQUE,
      user_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      subject TEXT NOT NULL,
      body TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'New',
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS ticket_replies (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id INTEGER NOT NULL,
      sender_id INTEGER NOT NULL,
      body TEXT NOT NULL,
      internal INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,
      FOREIGN KEY(ticket_id) REFERENCES tickets(id),
      FOREIGN KEY(sender_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS audit_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      action TEXT NOT NULL,
      detail TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    for code, nd, ne in CURRENCIES:
        db.execute("INSERT OR IGNORE INTO rates(code,name_dari,name_en,source) VALUES(?,?,?,'Not configured')", (code, nd, ne))
    db.commit()
    db.close()

def audit(action, detail):
    db = get_db()
    db.execute("INSERT INTO audit_log(user_id,action,detail,created_at) VALUES(?,?,?,?)",
               (session.get("user_id"), action, detail[:500], now()))
    db.commit()

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return get_db().execute("SELECT id,name,email,role,created_at FROM users WHERE id=?", (uid,)).fetchone()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("لطفاً ابتدا وارد حساب خود شوید.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                flash("لطفاً وارد شوید.", "warning")
                return redirect(url_for("login"))
            if user["role"] not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator

def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(24)
    return session["_csrf"]

@app.context_processor
def inject_globals():
    return {"business": BUSINESS, "current_user": current_user(), "csrf_token": csrf_token,
            "year": datetime.now().year}

@app.before_request
def protect_post():
    if request.method == "POST":
        token = session.get("_csrf", "")
        supplied = request.form.get("_csrf", "")
        if not token or not supplied or not hmac.compare_digest(token, supplied):
            abort(400, "درخواست نامعتبر است. صفحه را تازه‌سازی کرده و دوباره تلاش کنید.")

@app.template_filter("money")
def money(value):
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return "—"

@app.route("/")
def index():
    rates = get_db().execute("SELECT * FROM rates ORDER BY CASE code WHEN 'USD' THEN 0 WHEN 'EUR' THEN 1 WHEN 'GBP' THEN 2 WHEN 'PKR' THEN 3 ELSE 4 END, code").fetchall()
    return render_template("index.html", rates=rates)

@app.route("/rates")
def rates_page():
    rates = get_db().execute("SELECT * FROM rates ORDER BY code").fetchall()
    return render_template("rates.html", rates=rates)

@app.route("/convert", methods=["GET", "POST"])
def convert():
    result = None
    if request.method == "POST":
        try:
            code = request.form.get("currency", "").upper()
            amount = float(request.form.get("amount", ""))
            direction = request.form.get("direction", "BUY")
            if not (amount > 0 and amount < 1_000_000_000):
                raise ValueError
            rate = get_db().execute("SELECT * FROM rates WHERE code=?", (code,)).fetchone()
            if not rate or not rate["buy_rate"] or not rate["sell_rate"]:
                flash("نرخ این ارز هنوز توسط مدیر تنظیم نشده است.", "warning")
            else:
                selected = float(rate["sell_rate"] if direction == "BUY" else rate["buy_rate"])
                result = {"currency": code, "amount": amount, "rate": selected,
                          "total": amount * selected, "direction": direction}
        except (ValueError, TypeError):
            flash("مقدار و ارز را درست انتخاب کنید.", "danger")
    currencies = get_db().execute("SELECT * FROM rates WHERE code != 'AFN' ORDER BY code").fetchall()
    return render_template("convert.html", currencies=currencies, result=result)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if len(name) < 2 or len(name) > 100 or "@" not in email or len(password) < 10:
            flash("نام و ایمیل معتبر وارد کنید. رمز عبور باید حداقل ۱۰ حرف باشد.", "danger")
            return render_template("register.html")
        db = get_db()
        try:
            cur = db.execute("INSERT INTO users(name,email,password_hash,role,created_at) VALUES(?,?,?,'customer',?)",
                             (name, email, hash_password(password), now()))
            db.commit()
            session.clear()
            session["user_id"] = cur.lastrowid
            session["_csrf"] = secrets.token_urlsafe(24)
            audit("customer_register", f"New customer id={cur.lastrowid}")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("این ایمیل قبلاً ثبت شده است.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and verify_password(password, user["password_hash"]):
            session.clear()
            session["user_id"] = user["id"]
            session["_csrf"] = secrets.token_urlsafe(24)
            audit("login", f"Successful login for user id={user['id']}")
            return redirect(url_for("admin") if user["role"] in ("admin","staff","support","auditor") else url_for("dashboard"))
        flash("ایمیل یا رمز عبور نادرست است.", "danger")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    db = get_db()
    reqs = db.execute("SELECT * FROM requests WHERE user_id=? ORDER BY id DESC LIMIT 30", (user["id"],)).fetchall()
    tickets = db.execute("SELECT * FROM tickets WHERE user_id=? ORDER BY id DESC LIMIT 20", (user["id"],)).fetchall()
    conv = db.execute("SELECT * FROM conversations WHERE user_id=? ORDER BY id DESC LIMIT 1", (user["id"],)).fetchone()
    messages = []
    if conv:
        messages = db.execute("""SELECT m.*,u.name AS sender_name FROM messages m JOIN users u ON u.id=m.sender_id
                                WHERE conversation_id=? ORDER BY m.id ASC""", (conv["id"],)).fetchall()
    return render_template("dashboard.html", user=user, requests=reqs, tickets=tickets, messages=messages, conversation=conv)

@app.route("/request", methods=["GET", "POST"])
@login_required
def new_request():
    db = get_db()
    currencies = db.execute("SELECT * FROM rates WHERE code != 'AFN' ORDER BY code").fetchall()
    if request.method == "POST":
        direction = request.form.get("direction", "BUY")
        code = request.form.get("currency", "").upper()
        note = request.form.get("note", "").strip()[:1000]
        try:
            amount = float(request.form.get("amount", ""))
            if direction not in ("BUY","SELL") or not (0 < amount < 1_000_000_000):
                raise ValueError
            rate_row = db.execute("SELECT * FROM rates WHERE code=?", (code,)).fetchone()
            if not rate_row or not rate_row["buy_rate"] or not rate_row["sell_rate"]:
                flash("برای این ارز هنوز نرخ معتبر تنظیم نشده است.", "danger")
                return render_template("request.html", currencies=currencies)
            rate = float(rate_row["sell_rate"] if direction == "BUY" else rate_row["buy_rate"])
            total = amount * rate
            request_no = "SR-" + secrets.token_hex(4).upper()
            stamp = now()
            db.execute("""INSERT INTO requests(request_no,user_id,direction,currency,amount,rate,fee,total_afn,status,customer_note,created_at,updated_at)
                          VALUES(?,?,?,?,?,?, '0', ?, 'Submitted', ?, ?, ?)""",
                       (request_no, current_user()["id"], direction, code, f"{amount:.4f}", f"{rate:.6f}", f"{total:.2f}", note, stamp, stamp))
            db.commit()
            audit("request_created", request_no)
            flash(f"درخواست شما ثبت شد. شماره پیگیری: {request_no}. این درخواست هنوز معاملهٔ تکمیل‌شده نیست.", "success")
            return redirect(url_for("dashboard"))
        except (ValueError, TypeError):
            flash("مبلغ واردشده معتبر نیست.", "danger")
    return render_template("request.html", currencies=currencies)

@app.route("/message", methods=["POST"])
@login_required
def send_message():
    body = request.form.get("body", "").strip()
    if not body or len(body) > 3000:
        flash("پیام باید بین ۱ تا ۳۰۰۰ حرف باشد.", "danger")
        return redirect(url_for("dashboard"))
    db = get_db()
    user = current_user()
    conv = db.execute("SELECT * FROM conversations WHERE user_id=? ORDER BY id DESC LIMIT 1", (user["id"],)).fetchone()
    if not conv:
        cur = db.execute("INSERT INTO conversations(user_id,created_at) VALUES(?,?)", (user["id"], now()))
        conv_id = cur.lastrowid
    else:
        conv_id = conv["id"]
    db.execute("INSERT INTO messages(conversation_id,sender_id,body,created_at) VALUES(?,?,?,?)",
               (conv_id, user["id"], body, now()))
    db.commit()
    audit("message_sent", f"conversation={conv_id}")
    flash("پیام شما ارسال شد.", "success")
    return redirect(url_for("dashboard"))

@app.route("/support", methods=["GET", "POST"])
@login_required
def support():
    if request.method == "POST":
        category = request.form.get("category", "General")[:60]
        subject = request.form.get("subject", "").strip()[:150]
        body = request.form.get("body", "").strip()[:3000]
        if len(subject) < 3 or len(body) < 5:
            flash("عنوان و شرح مشکل را کامل وارد کنید.", "danger")
        else:
            db = get_db()
            ticket_no = "SUP-" + secrets.token_hex(4).upper()
            stamp = now()
            db.execute("""INSERT INTO tickets(ticket_no,user_id,category,subject,body,status,created_at,updated_at)
                          VALUES(?,?,?,?,?,'New',?,?)""",
                       (ticket_no, current_user()["id"], category, subject, body, stamp, stamp))
            db.commit()
            audit("support_ticket_created", ticket_no)
            flash(f"درخواست پشتیبانی ثبت شد. شماره پیگیری: {ticket_no}", "success")
            return redirect(url_for("dashboard"))
    return render_template("support.html")

@app.route("/admin")
@roles_required("admin","staff","support","auditor")
def admin():
    db = get_db()
    user = current_user()
    rates = db.execute("SELECT * FROM rates ORDER BY code").fetchall()
    requests = db.execute("""SELECT r.*,u.name AS customer_name FROM requests r JOIN users u ON u.id=r.user_id
                             ORDER BY r.id DESC LIMIT 100""").fetchall()
    transactions = db.execute("""SELECT t.*,u.name AS customer_name FROM transactions t LEFT JOIN users u ON u.id=t.user_id
                                 ORDER BY t.id DESC LIMIT 100""").fetchall()
    tickets = db.execute("""SELECT t.*,u.name AS customer_name FROM tickets t JOIN users u ON u.id=t.user_id
                            ORDER BY t.id DESC LIMIT 100""").fetchall()
    messages = db.execute("""SELECT m.*,u.name AS sender_name,c.user_id FROM messages m
                             JOIN users u ON u.id=m.sender_id JOIN conversations c ON c.id=m.conversation_id
                             ORDER BY m.id DESC LIMIT 100""").fetchall()
    stats = {
        "requests": db.execute("SELECT COUNT(*) FROM requests WHERE status NOT IN ('Completed','Rejected','Cancelled')").fetchone()[0],
        "transactions": db.execute("SELECT COUNT(*) FROM transactions WHERE status='Completed'").fetchone()[0],
        "tickets": db.execute("SELECT COUNT(*) FROM tickets WHERE status NOT IN ('Resolved','Closed')").fetchone()[0],
        "customers": db.execute("SELECT COUNT(*) FROM users WHERE role='customer'").fetchone()[0],
    }
    return render_template("admin.html", rates=rates, requests=requests, transactions=transactions, tickets=tickets,
                           messages=messages, stats=stats, role=user["role"])

@app.route("/admin/setup", methods=["GET", "POST"])
def admin_setup():
    # First administrator bootstrap is only allowed when no admin exists.
    db = get_db()
    admin_exists = db.execute("SELECT 1 FROM users WHERE role='admin' LIMIT 1").fetchone()
    if admin_exists:
        abort(404)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        setup_key = request.form.get("setup_key", "")
        expected = os.environ.get("SHARIFI_SETUP_KEY", "")
        if not expected or not hmac.compare_digest(setup_key, expected):
            flash("کلید راه‌اندازی مدیر درست نیست. ابتدا SHARIFI_SETUP_KEY را در محیط تنظیم کنید.", "danger")
        elif len(name) < 2 or "@" not in email or len(password) < 14:
            flash("نام و ایمیل معتبر وارد کنید؛ رمز عبور مدیر باید حداقل ۱۴ حرف باشد.", "danger")
        else:
            try:
                cur = db.execute("INSERT INTO users(name,email,password_hash,role,created_at) VALUES(?,?,?,'admin',?)",
                                 (name, email, hash_password(password), now()))
                db.commit()
                session.clear()
                session["user_id"] = cur.lastrowid
                session["_csrf"] = secrets.token_urlsafe(24)
                audit("admin_bootstrap", f"Initial administrator id={cur.lastrowid}")
                return redirect(url_for("admin"))
            except sqlite3.IntegrityError:
                flash("این ایمیل قبلاً ثبت شده است.", "danger")
    return render_template("admin_setup.html")

@app.route("/admin/rates", methods=["POST"])
@roles_required("admin","staff")
def update_rate():
    code = request.form.get("code", "").upper()
    source = request.form.get("source", "Administrator entered")[:120]
    try:
        buy = float(request.form.get("buy_rate", ""))
        sell = float(request.form.get("sell_rate", ""))
        if not (0 < buy < 1_000_000_000 and 0 < sell < 1_000_000_000):
            raise ValueError
    except (ValueError, TypeError):
        flash("نرخ خرید و فروش باید اعداد مثبت و معتبر باشند.", "danger")
        return redirect(url_for("admin"))
    db = get_db()
    row = db.execute("SELECT * FROM rates WHERE code=?", (code,)).fetchone()
    if not row or code == "AFN":
        flash("ارز انتخاب‌شده معتبر نیست.", "danger")
        return redirect(url_for("admin"))
    stamp = now()
    db.execute("UPDATE rates SET buy_rate=?,sell_rate=?,updated_at=?,updated_by=?,source=? WHERE code=?",
               (f"{buy:.6f}", f"{sell:.6f}", stamp, current_user()["id"], source, code))
    db.execute("INSERT INTO rate_history(code,buy_rate,sell_rate,source,changed_at,changed_by) VALUES(?,?,?,?,?,?)",
               (code, f"{buy:.6f}", f"{sell:.6f}", source, stamp, current_user()["id"]))
    db.commit()
    audit("rate_updated", f"{code}: buy={buy}; sell={sell}; source={source}")
    flash(f"نرخ {code} ذخیره شد.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/request/<int:request_id>", methods=["POST"])
@roles_required("admin","staff")
def update_request(request_id):
    status = request.form.get("status", "")
    allowed = {"Under Review","Awaiting Customer Confirmation","Approved","Rejected","Cancelled"}
    if status not in allowed:
        abort(400)
    db = get_db()
    req = db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
    if not req:
        abort(404)
    db.execute("UPDATE requests SET status=?,updated_at=? WHERE id=?", (status, now(), request_id))
    db.commit()
    audit("request_status_changed", f"{req['request_no']} -> {status}")
    flash("وضعیت درخواست به‌روزرسانی شد.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/complete/<int:request_id>", methods=["POST"])
@roles_required("admin","staff")
def complete_request(request_id):
    db = get_db()
    req = db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
    if not req:
        abort(404)
    if req["status"] in ("Completed","Rejected","Cancelled"):
        flash("این درخواست قبلاً بسته شده یا قابل تکمیل نیست.", "danger")
        return redirect(url_for("admin"))
    stamp = now()
    txn = "TX-" + secrets.token_hex(5).upper()
    receipt = "RC-" + secrets.token_hex(5).upper()
    db.execute("""INSERT INTO transactions(transaction_no,receipt_no,request_id,user_id,direction,currency,amount,rate,fee,total_afn,status,staff_id,created_at,note)
                  VALUES(?,?,?,?,?,?,?,?,?,?,'Completed',?,?,?)""",
               (txn, receipt, req["id"], req["user_id"], req["direction"], req["currency"], req["amount"], req["rate"],
                req["fee"], req["total_afn"], current_user()["id"], stamp, "ثبت‌شده توسط کارمند مجاز"))
    db.execute("UPDATE requests SET status='Completed',updated_at=? WHERE id=?", (stamp, request_id))
    db.commit()
    audit("transaction_completed", f"{txn}; receipt={receipt}")
    flash(f"معامله ثبت شد. شماره رسید: {receipt}", "success")
    return redirect(url_for("receipt", transaction_no=txn))

@app.route("/receipt/<transaction_no>")
@login_required
def receipt(transaction_no):
    db = get_db()
    txn = db.execute("""SELECT t.*,u.name AS customer_name,u.email AS customer_email,s.name AS staff_name
                        FROM transactions t LEFT JOIN users u ON u.id=t.user_id
                        JOIN users s ON s.id=t.staff_id WHERE t.transaction_no=?""", (transaction_no,)).fetchone()
    if not txn:
        abort(404)
    user = current_user()
    if user["role"] not in ("admin","staff","auditor") and txn["user_id"] != user["id"]:
        abort(403)
    return render_template("receipt.html", txn=txn)

@app.route("/admin/ticket/<int:ticket_id>", methods=["POST"])
@roles_required("admin","support")
def update_ticket(ticket_id):
    status = request.form.get("status", "In Progress")
    if status not in ("New","Open","In Progress","Waiting for Customer","Resolved","Closed"):
        abort(400)
    db = get_db()
    ticket = db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
    if not ticket:
        abort(404)
    db.execute("UPDATE tickets SET status=?,updated_at=? WHERE id=?", (status, now(), ticket_id))
    body = request.form.get("reply", "").strip()[:3000]
    if body:
        db.execute("INSERT INTO ticket_replies(ticket_id,sender_id,body,internal,created_at) VALUES(?,?,?,0,?)",
                   (ticket_id, current_user()["id"], body, now()))
    db.commit()
    audit("ticket_updated", f"{ticket['ticket_no']} -> {status}")
    flash("درخواست پشتیبانی به‌روزرسانی شد.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/message/<int:conversation_id>", methods=["POST"])
@roles_required("admin","staff","support")
def reply_message(conversation_id):
    body = request.form.get("body", "").strip()
    if not body or len(body) > 3000:
        flash("متن پیام معتبر نیست.", "danger")
        return redirect(url_for("admin"))
    db = get_db()
    conv = db.execute("SELECT * FROM conversations WHERE id=?", (conversation_id,)).fetchone()
    if not conv:
        abort(404)
    db.execute("INSERT INTO messages(conversation_id,sender_id,body,created_at) VALUES(?,?,?,?)",
               (conversation_id, current_user()["id"], body, now()))
    db.commit()
    audit("staff_message_reply", f"conversation={conversation_id}")
    flash("پاسخ پیام ارسال شد.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/export.csv")
@roles_required("admin","auditor")
def export_csv():
    rows = get_db().execute("""SELECT transaction_no,receipt_no,direction,currency,amount,rate,fee,total_afn,status,created_at
                               FROM transactions ORDER BY id DESC""").fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["transaction_no","receipt_no","direction","currency","amount","rate","fee","total_afn","status","created_at"])
    for row in rows:
        writer.writerow(list(row))
    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=sharifi-transactions.csv"
    return response

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(403)
def forbidden(_error):
    return render_template("error.html", code=403, message="شما اجازهٔ دسترسی به این بخش را ندارید."), 403

@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404, message="صفحه یا مورد درخواستی پیدا نشد."), 404

@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400, message=getattr(error, "description", "درخواست نامعتبر است.")), 400

init_db()

if __name__ == "__main__":
    # Local development only. Use a production WSGI server and HTTPS in production.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
