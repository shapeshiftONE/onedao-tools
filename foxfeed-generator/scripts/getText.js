const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY)
const Crawler = require('crawler');
const c = new Crawler({
  maxConnections: 3,
  // This will be called for each crawled page
  callback: (error, res, done) => {
      if (error) {
          console.log(error);
      } else {
          const $ = res.$;
      }
      done();
  }
});
async function getArticles(){
    const { data, error } = await supabase
    .from('feed_articles')
    .select(`
        url,
        publisher (
            fullSelector,
            url
        )
  `)
    //   .eq('fullText', null)

    return data
  }

async function scrapeArticle(){
    const articles = await getArticles();
    for (const article of articles) {
        console.log(article['publisher']['url'])
          
        const selector = article['publisher']['fullSelector']
        c.queue({
            uri: article['url'],
            rotateUA: true,
            referer: article['publisher']['url'],
            callback: (error, res, done) => {
                if (error) {
                    console.log(error);
                } else {
                    try{
                        const $ = res.$;
                        const theText = $(selector).html()
                            .replace(/(\r\n|\n|\r)/gm, "")
                            .replace(/style=\"[^\"]*\"/g, "")
                            .replace(/class=\"[^\"]*\"/g, "");
                            (async() => {
                            const { data, error2 } = await supabase
                            .from('feed_articles')
                            .update({ fullText: theText })
                            .eq('url', article['url'])
                        })()
                    }   catch (err) {
                        console.error(err);
                      }

                }


                done();
            }
    }
        );
}
}

  scrapeArticle()