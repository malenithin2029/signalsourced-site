from pathlib import Path

p = Path('index.html')
text = p.read_text()

old_form = '<form id="pilot-form" novalidate>'
new_form = '<form id="pilot-form" action="https://formspree.io/f/mqpazejk" method="POST" novalidate>\n                <input type="hidden" name="_subject" value="New SignalSourced Founding Partner Application" />\n                <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0;pointer-events:none" />'
text = text.replace(old_form, new_form)

text = text.replace(
    '.preview{display:inline-block;margin-top:14px;font-size:13px;color:var(--w-text);background:var(--warm-soft);border:1px solid rgba(var(--w-rgb),.3);padding:8px 12px;border-radius:10px}',
    '.preview{display:inline-block;margin-top:14px;font-size:13px;color:var(--accent-2);background:rgba(var(--a-rgb),.08);border:1px solid rgba(var(--a-rgb),.28);padding:8px 12px;border-radius:10px}'
)

text = text.replace(
    'Preview mode: your application has not been sent yet. We will connect the live form before the public launch.',
    'Application sent successfully. We’ll review the details and reply by email if the founding pilot looks like a fit.'
)

start = text.index("    form.addEventListener('submit', e => {")
end = text.index("    $('#s-edit').addEventListener", start)

new_submit = '''    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (fi < steps.length - 1) { next.click(); return; }
      const bad = steps.findIndex(s => fieldsIn(s).some(el => !el.checkValidity()));
      if (bad !== -1) {
        showStep(bad); validateStep(steps[bad]);
        status.textContent = 'Please complete the required fields above.';
        return;
      }

      const val = id => $('#' + id).value.trim();
      const rows = [['Name', val('name')], ['Work email', val('email')], ['Website', val('website')], ['Team size', val('team')], ['Project value', val('project-value')], ['Capacity', val('capacity')], ['Ideal client', val('ideal-client')], ['Clients today', val('pipeline')]];
      const originalSubmit = submit.innerHTML;
      submit.disabled = true;
      submit.setAttribute('aria-busy', 'true');
      submit.textContent = 'Sending application…';
      status.textContent = 'Sending your application securely…';

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) throw new Error('Form submission failed');

        $('#s-name').textContent = val('name').split(' ')[0] || 'there';
        const dl = $('#s-summary'); dl.innerHTML = '';
        rows.filter(r => r[1]).forEach(([k, v]) => {
          const row = document.createElement('div'), dt = document.createElement('dt'), dd = document.createElement('dd');
          dt.textContent = k; dd.textContent = v; row.append(dt, dd); dl.appendChild(row);
        });
        form.hidden = true;
        success.hidden = false;
        success.focus();
        status.textContent = '';
      } catch (error) {
        status.textContent = 'We could not send the application. Please check your connection and try again.';
      } finally {
        submit.disabled = false;
        submit.removeAttribute('aria-busy');
        submit.innerHTML = originalSubmit;
      }
    });
'''

text = text[:start] + new_submit + text[end:]
p.write_text(text)
print('Formspree connected')
