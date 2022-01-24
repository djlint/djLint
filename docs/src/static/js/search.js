// var client = algoliasearch('QFXNLHI6NP', '6b5ccc86ead48e79e587963eeb2d83e8');
// var searchIndex = client.initIndex("dev_atlas");

// var searchBox = document.getElementById("search");
// var searchForm = document.getElementById("search-form");

// var runSearch = function(event) {
//   var searchResultsContainer = document.getElementById("search-results");
//   searchResultsContainer.textContent = "";

//   var searchTerm = event.target.value;
//   if (searchTerm.length < 2) return;

//   var toolToFilterBy = event.target.dataset.filter || false;

//   var alogliaArgs = {
//     hitsPerPage: 10,
//     attributesToRetrieve: ["title", "url", "_tags"],
//     attributesToSnippet: ["content"],
//     snippetEllipsisText: "…",
//   };

//   if (toolToFilterBy) alogliaArgs.filters = toolToFilterBy;

//   searchIndex.search(searchTerm, alogliaArgs).then(function(e){
//     results = e["hits"]

//     console.log(results);

//   var formattedResults = results.map(function(result){
//     var toolName = extractToolName(result._tags);
//     console.log(toolName)
//     // Create elements
//     var link = document.createElement("a");
//     var title = document.createElement("strong");
//     var excerpt = document.createElement("p");
//     var tool = document.createElement("span");

//     link.href = result.url;
//     link.classList.add(
//       "panel-block",
//       "p-3",
//       "is-block"
//     );

//     excerpt.classList.add("search-snippet");
//     excerpt.innerHTML = result._snippetResult.content.value;

//     title.classList.add("is-flex", "is-justify-content-space-between");
//     title.innerText = result.title;

//     tool.innerText = toolName;
//     tool.classList.add(
//       "tag",
//       "is-info",
//       "is-light"

//     );

//     // Put all the elements together
//     title.appendChild(tool);
//     link.appendChild(title);
//     link.appendChild(excerpt);
//     return link;
//    });

//   formattedResults.map(function(el){
//     searchResultsContainer.insertAdjacentElement("beforeend", el)
//   });
// });
// };

// var extractToolName = function(tags) {
//   return tags.filter(function(tag){ return tag === "BI Library" || tag === "Automation Hub" || tag === "Atlas"});
// };

// Function.prototype.debounce = function (delay) {
//   var outter = this,
//     timer;

//   return function () {
//     var inner = this,
//       args = [].slice.apply(arguments);

//     clearTimeout(timer);
//     timer = setTimeout(function () {
//       outter.apply(inner, args);
//     }, delay);
//   };
// };

// if(searchBox != undefined || searchForm != undefined){
//   searchBox.addEventListener("input", runSearch.debounce(250));
//   searchForm.addEventListener("submit", (e) => e.preventDefault());
// }
