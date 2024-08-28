module.exports = {
  type: "page",
  meta: {
    site: {
      name: (data) => data.site.title,
      description: (data) => data.site.description,
      url: (data) => data.site.url,
      logo: {
        src: (data) => data.site.image,
      },
    },
    language: "en-US",
    url: (data) => data.site.url + data.page.url,
    title: (data) => data.title || data.site.title,
    description: (data) => data.description || data.site.description,
    image: {
      src: (data) => data.page.image,
    },
    modified: (data) => data.page.date.toISOString(),
    keywords: (data) => data.keywords,
  },
};
