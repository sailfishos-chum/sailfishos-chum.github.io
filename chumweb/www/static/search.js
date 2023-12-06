class SearchForm extends HTMLFormElement {

    /**
     * @type {null|HTMLInputElement} Search element
     */
    search = null
    /**
     * @type {HTMLDivElement|null}
     */
    resultsContainer = null
    static index = null
    static lunrIndex = null
    static packages = null

    constructor() {
        self = super();
        this.self = self
    }

    /**
     * Retrieve the search query from the URL
     * @returns {null|string} The query
     */
    static getSearchQuery() {
        return new URLSearchParams(window.location.search).get("q")
    }

    connectedCallback() {
        console.log("SearchForm connectedCallback", this)
        window.requestAnimationFrame(() => {
            this.updateQueryField()
        })
    }

    updateQueryField() {
        this.search = this.querySelector("input[type=search]")

        if (this.search) {
            this.search.value = SearchForm.getSearchQuery()
        } else {
        }
    }

    ensureIndexLoaded() {
        if (SearchForm.index) {
            return Promise.resolve()
        }
        return fetch(window.publicUrl + "/packages-index.json")
            .then((response) => {
                return response.json()
            })
            .then((index) => {
                SearchForm.index = index
                SearchForm.lunrIndex = lunr.Index.load(index)
                return Promise.resolve()
            })
            .then(() => {
                return fetch(window.publicUrl + "/packages.json")
            })
            .then((response) => {
                return response.json()
            })
            .then((packages) => {
                SearchForm.packages = packages;
                return Promise.resolve()
            })
            .catch((error) => alert("Error while searching: " + error.toString()))
    }

    doSearch(query) {
        this._clearResults()
        document.getElementById("search-results-busy").style.display = "block";

        let self = this;
        this.ensureIndexLoaded()
            .then(() => {
                let matches = SearchForm.lunrIndex.search(query)
                let results = SearchForm.packages
                    .map(pkg => {
                        pkg.match = matches.find(m => m.ref === pkg.name)
                        return pkg
                    })
                    .filter(pkg => pkg.match)
                    .sort((l, r) => r.match.score - l.match.score)
                console.log(results)
                self.updateResults(results)
            })
    }

    _clearResults() {
        if (!this.resultsContainer) this.resultsContainer = document.getElementById("search-results")
        while (this.resultsContainer.firstChild) {
            this.resultsContainer.removeChild(this.resultsContainer.firstChild)
        }
        document.getElementById("search-results-empty").style.display = "none";
        document.getElementById("search-results-busy").style.display = "none";
        document.getElementById("search-results-no-query").style.display = "none";
    }


    /**
     * Updates the UI to show the search results
     * @param {Object[]} results The search results to show
     */
    updateResults(results) {
        let resultsContainer = document.getElementById("search-results")
        this._clearResults()
        document.getElementById("search-results-busy").style.display = "none";

        if (results.length === 0) {
            document.getElementById("search-results-empty").style.display = "block";
            return;
        }

        /**
         * @type {HTMLTemplateElement}
         */
        let resultTemplate = document.getElementById("search-result")

        for (const result of results) {
            let resultInstance = resultTemplate.content.cloneNode(true)

            let link = resultInstance.querySelector("a.pkg-title");
            link.textContent = result.title;
            link.href = result.url;

            let iconLink = resultInstance.querySelector("a.pkg-icon");
            iconLink.href = result.url;

            let pkgIcon = resultInstance.querySelector("picture.pkg-icon > source:first-child")
            pkgIcon.srcset = result.icon;

            resultInstance.querySelector(".pkg-summary").textContent = result.summary;

            let version = resultInstance.querySelector(".pkg-version")
            version.textContent = result.version_short;
            version.title = result.version;

            resultsContainer.appendChild(resultInstance);
        }
    }
}

customElements.define("search-form", SearchForm, {extends: "form"})

document.addEventListener("DOMContentLoaded", () => {
    let mainSearchForm = document.getElementById("main-search-form")
    let searchQuery = SearchForm.getSearchQuery()
    if (mainSearchForm && searchQuery) {
        mainSearchForm.doSearch(searchQuery)
    } else {
        document.getElementById("search-results-no-query").style.display = "block";
    }
})
