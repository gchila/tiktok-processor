/********************************************************************************/
// TIKTOK: EXPORT ANY TIKTOK CHANNEL VIDEO TITLES AND URLS TO TEXT/CSV/EXCEL/SPREADSHEET
// https://responsive-muse.com/2023/06/19/export-tiktok-channel-video-titles-urls-using-javascript/
// JAVASCRIPT CODE TO COPY & PASTE IN THE CONSOLE (F12) OF ANY WEB BROWSER. 
// TESTED IN CHROME IN JUNE 2023, BUT SHOULD WORK IN ANY WEB BROWSER.
// VIDEO TUTORIAL AND SUPPORT AVAILABLE AT https://www.youtube.com/@NetgrowsTech/
// CODE CREATED BY NETGROWS TECH. VISIT US AT https://responsive-muse.com & https://netgrows.com
/********************************************************************************/



    //1. Visit the TikTok channel page:

    //Example: https://www.tiktok.com/@google




    //2. Open the console (F12), paste the code 1 and press enter

    //COPY & PASTE CODE 1:

    let goToBottom = setInterval(() => window.scrollBy(0, 400), 1000);




    //3. Wait until the page scrolls to the bottom and then paste the code 2 and press enter

    //You can copy and paste this data into any spreadsheet or optionally download it as a CSV file (see step 4)

    //COPY & PASTE CODE 2:

    clearInterval(goToBottom);
    let arrayVideos = [];
    console.log('\n'.repeat(50));
    const containers = document.querySelectorAll('[class*="-DivItemContainerV2"]');  
    for (const container of containers) {
        const link = container.querySelector('[data-e2e="user-post-item"] a');
        const title = container.querySelector('[data-e2e="user-post-item-desc"] a');
        //If the link is https://www.tiktok.com/, set it as the current page URL
        if (link.href === 'https://www.tiktok.com/') link.href = window.location.href;
        arrayVideos.push(title.title + ';' + link.href);
        console.log(title.title + '\t' + link.href);
    }




    //4. (Optional) Download the results as a CSV file (using ; as separator)

    //COPY & PASTE CODE 3:

    let data = arrayVideos.join('\n');
    let blob = new Blob([data], {type: 'text/csv;charset=ISO-8859-1'});
    let elem = window.document.createElement('a');
    elem.href = window.URL.createObjectURL(blob);
    elem.download = 'urls.csv';
    document.body.appendChild(elem);
    elem.click();
    document.body.removeChild(elem);