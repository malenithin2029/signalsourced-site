from pathlib import Path
import json,re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
assert '<title>SignalSourced' in s and 'id="pilot-form"' in s and 'class="brand"' in s
s=s.replace('<title>SignalSourced — Signal-based outbound for B2B web agencies</title>','<title>SignalSourced | Signal-Based Lead Generation for B2B Web Agencies</title>',1)
s=s.replace('content="SignalSourced helps B2B web agencies find good-fit companies with relevant buying signals and start qualified sales conversations with the right decision-makers."','content="SignalSourced helps B2B web design and development agencies find qualified prospects using verified buying signals, decision-maker research and personalized outbound. Explore our 30-day founding pilot."',1)
oldfavicon=re.search(r'  <link rel="icon" href="data:image/svg\+xml,[^\n]+\n',s)
assert oldfavicon,'original favicon missing'
s=s[:oldfavicon.start()]+'  <link rel="icon" type="image/svg+xml" href="/logo-mark.svg" />\n'+s[oldfavicon.end():]
extra='''  <link rel="canonical" href="https://signalsourced.com/" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="SignalSourced" />
  <meta property="og:url" content="https://signalsourced.com/" />
  <meta property="og:title" content="SignalSourced | Signal-Based Lead Generation for B2B Web Agencies" />
  <meta property="og:description" content="Find good-fit accounts with verified signals, research the right decision-makers, and launch thoughtful outbound. Explore the SignalSourced founding pilot." />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="SignalSourced | Signal-Based Client Acquisition" />
  <meta name="twitter:description" content="Relevant B2B prospecting built around fit, verified signals and human-reviewed outreach." />
'''
assert 'rel="canonical"' not in s
s=s.replace('  <link rel="preconnect" href="https://fonts.googleapis.com" />',extra+'  <link rel="preconnect" href="https://fonts.googleapis.com" />',1)
structured={"@context":"https://schema.org","@graph":[{"@type":"Organization","@id":"https://signalsourced.com/#organization","name":"SignalSourced","url":"https://signalsourced.com/","logo":"https://signalsourced.com/logo-mark.svg","email":"inquiries@signalsourced.com","description":"Signal-based B2B client acquisition for web design and development agencies."},{"@type":"WebSite","@id":"https://signalsourced.com/#website","name":"SignalSourced","url":"https://signalsourced.com/","publisher":{"@id":"https://signalsourced.com/#organization"}},{"@type":"Service","@id":"https://signalsourced.com/#pilot","name":"Signal-Based Pipeline Sprint","serviceType":"B2B prospect research and personalized outbound for web agencies","provider":{"@id":"https://signalsourced.com/#organization"},"description":"A 30-day founding pilot for established B2B web design and development agencies, including ICP definition, signal research, decision-maker research, human-reviewed outreach and reporting.","url":"https://signalsourced.com/#pilot","offers":{"@type":"Offer","price":"750","priceCurrency":"USD","description":"Advertised 30-day founding pilot; subject to acceptance, a separate agreement and agreed client-owned infrastructure costs."}}]}
s=s.replace("  <script>document.documentElement.classList.add('js')</script>",'  <script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+"</script>\n  <script>document.documentElement.classList.add('js')</script>",1)
pattern=r'(<span class="logo" aria-hidden="true">)<svg\b.*?</svg>(</span>)'
assert len(re.findall(pattern,s,flags=re.S))==1,'expected exactly one navbar artwork'
s=re.sub(pattern,r'\1<img src="/logo-mark.svg" alt="" width="28" height="28" style="display:block;width:28px;height:28px" />\2',s,count=1,flags=re.S)
if 'id="agency-summary"' not in s:
    anchor='    <!-- APPLY -->'
    assert anchor in s
    block='''    <section id="agency-summary" class="section" aria-labelledby="agency-summary-title" style="padding:32px 0 50px"><div class="wrap"><div class="card" style="padding:28px 32px"><div class="kicker">At a glance</div><h2 id="agency-summary-title" style="font-size:clamp(24px,3vw,34px)">What does SignalSourced do?</h2><p class="sub">SignalSourced is a signal-based B2B lead generation and outbound service for web design and development agencies. We identify companies that fit an agency's ideal customer profile, verify relevant public buying signals, research suitable decision-makers, and develop personalized outreach with human review. Our 30-day founding pilot costs $750, with any separately agreed client-owned infrastructure or data expenses excluded. We do not guarantee meetings or revenue.</p><p style="margin:16px 0 0"><a href="#method" style="color:var(--accent);text-decoration:underline">Explore the method</a> · <a href="#pilot" style="color:var(--accent);text-decoration:underline">Read the pilot details</a> · <a href="mailto:inquiries@signalsourced.com" style="color:var(--accent);text-decoration:underline">Contact us</a></p></div></div></section>

'''
    s=s.replace(anchor,block+anchor,1)
p.write_text(s,encoding='utf-8')
for name,desc in [('privacy.html','Privacy Notice'),('terms.html','Website Terms')]:
    q=Path(name)
    t=q.read_text(encoding='utf-8')
    canonical=f'  <link rel="canonical" href="https://signalsourced.com/{name}" />'
    if 'rel="canonical"' not in t:
        t=t.replace('<title>'+desc+' | SignalSourced</title>','<title>'+desc+' | SignalSourced</title>'+canonical,1)
    q.write_text(t,encoding='utf-8')
print('SEO upgrade applied:',len(s),'bytes; metadata, structured data, radar logo, descriptive summary and policy canonicals')
