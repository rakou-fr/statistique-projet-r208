const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

puppeteer.use(StealthPlugin()); // 🔥 Mode furtif activé

async function getRandomProxy(csvFilePath) {
    return new Promise((resolve, reject) => {
        const proxies = [];
        fs.createReadStream(csvFilePath)
            .pipe(csv())
            .on('data', (row) => {
                proxies.push(row);
            })
            .on('end', () => {
                if (proxies.length === 0) {
                    return reject(new Error("Aucun proxy trouvé dans le fichier CSV"));
                }
                const randomProxy = proxies[Math.floor(Math.random() * proxies.length)];
                resolve(randomProxy);
            })
            .on('error', reject);
    });
}

async function fetchAllCookiesAndData(searchParams) {
    try {
        // const csvFilePath = path.join(__dirname, './Files/proxys.csv');
        // const proxy = await getRandomProxy(csvFilePath);

        // console.log(`[INFO] Utilisation du proxy : ${proxy.ip}:${proxy.port}`);

        const browser = await puppeteer.launch({
            headless: true,
            args: [
                // `--proxy-server=${proxy.ip}:${proxy.port}`,
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-blink-features=AutomationControlled',
                '--disable-gpu',
                '--dns-prefetch-disable',
                '--incognito'
            ]
        });

        const page = await browser.newPage();

        // if (proxy.login && proxy.mdp) {
        //     console.log(`[INFO] Authentification avec : ${proxy.login}`);
        //     await page.authenticate({
        //         username: proxy.login,
        //         password: proxy.mdp
        //     });
        // }

        await page.evaluateOnNewDocument(() => {
            Object.defineProperty(navigator, 'connection', { get: () => undefined });
            Object.defineProperty(navigator, 'webkitConnection', { get: () => undefined });
            Object.defineProperty(navigator, 'mozConnection', { get: () => undefined });
        });

        console.log("[INFO] Connexion à Vinted...");
        await page.goto('https://www.vinted.fr', { waitUntil: 'load' });

        const cookies = await page.cookies();
        const cookieStr = cookies.map(cookie => `${cookie.name}=${cookie.value}`).join('; ');

        console.log(`[INFO] Cookies récupérés via Puppeteer : ${cookieStr}`);

        const apiUrl = `https://www.vinted.fr/api/v2/catalog/items?${searchParams.toString()}&per_page=960`;
        

        console.log(`[INFO] Navigation vers l'API : ${apiUrl}`);

        // Aller sur l'URL de l'API Vinted et attendre la réponse
        await page.setExtraHTTPHeaders({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Cookie': cookieStr
        });

        await page.goto(apiUrl, { waitUntil: 'networkidle2' });

        const jsonData = await page.evaluate(() => {
            return JSON.parse(document.body.innerText);
        });

        console.log("[INFO] Données récupérées avec succès !");
        // console.log(jsonData);

        await browser.close();
        // return jsonData;
        const JSONToFile = (obj, filename) =>
            fs.writeFileSync(`${filename}.json`, JSON.stringify(obj, null, 2));

        JSONToFile(jsonData, 'H&M');

        console.log("GOODA");

    } catch (error) {
        console.error(`[ERREUR] ${error.message}`);
        return null;
    }
}


fetchAllCookiesAndData("search_text=h%26m pull&time=1742371542&catalog[]=79&page=1&brand_ids[]=7&status_ids[]=6&status_ids[]=1");