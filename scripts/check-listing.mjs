#!/usr/bin/env node
// Invariant: README, llms.txt and both manifests state one tool count, version and
// price line. With --live, that count must also equal tools/list on the live server.
// Node 18+, no dependencies. Exit 1 on any mismatch.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(join(root, p), 'utf8');
const META = 'io.modelcontextprotocol.registry/publisher-provided';
const errors = [];
const check = (ok, msg) => { if (!ok) errors.push(msg); };

const main = JSON.parse(read('manifests/energyai.server.json'));
const alias = JSON.parse(read('manifests/solar-home-incentives.server.json'));
const c = main._meta?.[META]?.toolCount;
check(c && c.total === c.noKey + c.freeWithKey + c.paid, 'toolCount parts must sum to total');
check(main.version === alias.version, 'manifest versions differ');
check(main.description.length <= 100, 'short description over 100 characters');
check(alias._meta?.[META]?.toolCount?.total === c.noKey, 'discovery alias count must equal the no-key count');
check(main.remotes[0].headers[0].description === main._meta[META].priceLine, 'header text must be the price line');

const readme = read('README.md');
const block = readme.split('<!-- tool-count:start')[1]?.split('<!-- tool-count:end -->')[0] ?? '';
check(block.includes(`**${c.total} tools:** ${c.noKey} work with no key`), 'README count block disagrees with manifest');
check(block.includes(main._meta[META].priceLine), 'README price line disagrees with manifest');
check(readme.includes(`${c.noKey} tools need no key to start`), 'README intro count disagrees');
check(readme.includes(`**v${main.version}**`), 'README manifest version disagrees');
check(read('llms.txt').includes(`Tools: ${c.total} in all. ${c.noKey} with no key, ${c.freeWithKey} more free with a free key, ${c.paid} paid`), 'llms.txt count disagrees');
const tableRows = (h) => (readme.split(h)[1] ?? '').split('\n### ')[0].split('\n').filter((l) => /^\| `/.test(l)).length;
check(tableRows('### No key: informational tools') + tableRows('always-free tools') === c.noKey, 'no-key tables do not list every no-key tool');
check(tableRows('### Free with a free key') === c.freeWithKey, 'free-with-key table count wrong');
check(tableRows('### Paid (') === c.paid, 'paid table count wrong');

if (process.argv.includes('--live')) {
  const url = main.remotes[0].url;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/list', params: {} }),
  });
  const tools = (await res.json()).result.tools;
  check(tools.length === c.total, `live server lists ${tools.length} tools, docs say ${c.total}`);
  const paid = tools.filter((t) => /\[\$\d+\.\d\d\/call\]$/.test(t.description)).length;
  check(paid === c.paid, `live server has ${paid} paid tools, docs say ${c.paid}`);
}

if (errors.length) { console.error(errors.map((e) => `✗ ${e}`).join('\n')); process.exit(1); }
console.log(`✓ listing consistent: ${c.total} tools = ${c.noKey} no key + ${c.freeWithKey} free with key + ${c.paid} paid (v${main.version})`);
