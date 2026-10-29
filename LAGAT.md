# Lagat av driftvakten
2026-10-29 | alla sajter | morgonkoll: alla 12 svarar 200, Vercel-teamet utan spärr, inga nya larm sedan 27 okt (ärende #17/#18 redan hanterade), Stripe-kopplingen kräver ny inloggning (ej läst) | inget att laga | –
2026-10-29 | sentry SAJTERNA-7 | RangeError (rekursion) i kommunradar.se, 3 händelser på 12 s, en iPhone-session (Chrome iOS), 0 användare; felraden finns inte längre på dagens sida | ej åtgärdat, lämnas öppen, bevakas | –
2026-10-29 | olles kö | lansera-kort för krimradar, konkursradarn, granntvisten (Adtraction-ansökningar väntar på Olle) | kort lagda | –
2026-10-27 | alla sajter | morgonkoll: alla 12 sajter svarar 200, Vercel-teamet utan spärr, Sentry tappar inget på kvot (Stripe-kopplingen kräver ny inloggning, kunde inte läsas) | inget att laga | –
2026-10-27 | konkursradarn, nordwikpartners | fart-varning v44 (83, 66): sidorna är lätta (90 resp. 18 kB), troligen mätbrus/extern bild; inget ändrat | väntar | –
2026-10-27 | sentry SAJTERNA-6 | fel från localhost:8471 (testkörning, inte skarp sajt) | ignoreras | –
2026-10-27 | länkkoll v44 | resten är falska larm (SCB geoserver 400, Brevo-formulär 400, 307, vinföretags-sajter); racepoint/nordwik/husradarn redan lagade på vantar-pa-olle | – | –
2026-10-22 | alla 8 Vercel-sajter | 402 sedan 20 okt 22:38 (obetald Vercel-faktura, teamet saasverket) – Olle betalade 22 okt, alla svarar 200, Vercel softBlock borta, status active | larmkedjan byggd: vakt.py mejlar Olle (@olleno + tilldelning) efter 15 min nere, var 6:e timme, ✅ när uppe; testat skarpt med testrad (ärende #14), mejlen kom fram; morgonrutinen kollar betalningar (Vercel/Sentry/Stripe) och mejlar Olle varje morgon tills löst | main
2026-10-22 | agentvakt | körningen fallerade vid "Spara översikten" (push krockade med andra chattar) → ~200 Run failed-mejl | pull --rebase + 5 försök, fallerar aldrig på det steget | main
2026-10-22 | sajtvakt | KVAR: GitHubs schema kör vakten bara var 3–5:e timme (inte var 5:e min); Gmail-filtret "Nyhetsbrev" gömmer GitHubs ärendemejl | väntar på Olles beslut (klocka i Cloudflare + nyckel; ändra filtret) | –
2026-10-21 | saasverket, finansieringsverket, investeringsverket, dejtradar, krimradar, konkursradarn, granntvisten, husradarn | alla svarar 402 DEPLOYMENT_DISABLED (Vercel-kontot saasverket, inte koden; senaste deploy READY) | ej lagat i kod, notis till Olle | –
2026-10-20 | racepoint | död bild kommunradar.se/logo.svg (404) | sponsorraden visar namnet i text; bygge/test kunde inte köras här (bygget kräver data) | vantar-pa-olle
2026-10-20 | nordwikpartners-web | död länk investindalarna.se …facebook-datahall-sweco.pdf (404) | länken borttagen, texten kvar (2 ställen); sidtester OK | vantar-pa-olle
2026-10-20 | investverket | död källänk etoro.com/sv/investing/stocks (404) | borttagen ur data/produkter/etoro.json, ombyggd, alla tester OK | vantar-pa-olle
2026-10-20 | husradarn | döda länkar Skatteverket fastighetstaxering och Svenskt Vatten-rapporten (404) | bytta till skatteverket.se/…/fastighetstaxering och taxestatistik-xlsx, ombyggd, tester OK | vantar-pa-olle
2026-10-20 | wineradar-bygg | fart 84→65 (larm #4) | ej åtgärdat, behöver egen utredning | –
2026-10-20 | (ej lagat) | 307/303/525-svar, vinföretagens egna sajter nere, Amazon 503 | inga riktiga fel hos oss | –

