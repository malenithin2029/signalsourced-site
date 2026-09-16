from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old_footer = '<footer class="footer"><div class="wrap footerin"><div><strong>SignalSourced</strong> · Signal-based outbound for B2B web agencies.</div><div class="values"><span>Relevance over volume</span><span>Evidence over assumptions</span><span>Human judgment in the loop</span></div></div></footer>'
new_footer = '<footer class="footer"><div class="wrap footerin"><div><strong>SignalSourced</strong> · Signal-based outbound for B2B web agencies.<div style="margin-top:12px;font-size:14px;display:flex;gap:16px;flex-wrap:wrap"><a href="mailto:inquiries@signalsourced.com">inquiries@signalsourced.com</a><a href="/privacy.html">Privacy Notice</a><a href="/terms.html">Website Terms</a></div></div><div class="values"><span>Relevance over volume</span><span>Evidence over assumptions</span><span>Human judgment in the loop</span><a href="https://calendly.com/nithin-signalsourced/signalsourced-discovery-call" target="_blank" rel="noopener noreferrer" style="text-decoration:underline;text-underline-offset:3px">Already invited? Book a discovery call ↗</a></div></div></footer>'
if old_footer not in html:
    raise SystemExit('Original footer not found: website left unchanged')
html = html.replace(old_footer, new_footer, 1)

old_form = '<form id="pilot-form" action="https://formspree.io/f/mqpazejk" method="POST" novalidate>'
new_form = old_form + '\n              <p style="font-size:13px;line-height:1.65;color:var(--muted);margin:0 0 16px">We use the information you submit to review your application and reply. Read our <a href="/privacy.html" target="_blank" rel="noopener noreferrer" style="color:var(--accent-2);text-decoration:underline">Privacy Notice</a>. Applying does not create a client agreement; see our <a href="/terms.html" target="_blank" rel="noopener noreferrer" style="color:var(--accent-2);text-decoration:underline">Website Terms</a>.</p>'
if old_form not in html:
    raise SystemExit('Application form not found: website left unchanged')
html = html.replace(old_form, new_form, 1)

# Clarify manual qualification and how invited prospects can schedule.
old_success = 'Application sent successfully. We’ll review the details and reply by email if the founding pilot looks like a fit.'
new_success = 'Application sent successfully. We’ll review the details and reply by email if the founding pilot looks like a fit. If we invite you to a discovery call, we’ll send you the booking link.'
if old_success not in html:
    raise SystemExit('Expected success message not found: website left unchanged')
html = html.replace(old_success, new_success, 1)

assert html.count('inquiries@signalsourced.com') >= 1
assert 'https://formspree.io/f/mqpazejk' in html
assert 'https://calendly.com/nithin-signalsourced/signalsourced-discovery-call' in html
path.write_text(html, encoding='utf-8')
print('Updated footer, application disclosure and qualified booking workflow')
