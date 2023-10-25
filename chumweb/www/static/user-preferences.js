/**
 * Class for saving, loading and applying user preferences.
 */
function UserPreferences() {
    this.prefs = {
        architecture: {
            default: "aarch64",
            current: null,
            /// Find the closest match for the available options that matches this preference's value
            findBestOption: (options, preferredValue) => {
                console.log("findBestOption: ", options, preferredValue)
                if (options.indexOf(preferredValue) >= 0) {
                    // Check if our preferred architecture is available
                    return preferredValue;
                } else if (options.indexOf("noarch") >= 0) {
                    // Otherwise, noarch has preference
                    return "noarch";
                } else if (options.length > 0) {
                    // Just pick the first I suppose
                    return options[0];
                }
                return undefined;
            },
            allowSavePref: function(value) {
                // noarch is not a valid preferred architecture :p.
                // Packages have either multiple architecture or a "noarch". To prevent users from
                // accidentally setting their preferred architecture to "noarch" when visiting a package
                // that is architecture independent.
                return value !== "noarch";
            }
        }
    }
}

/**
 * Loads all preferences from browser local storage or populates them with default values
 */
UserPreferences.prototype.loadPrefs = function() {
    for (const pref in this.prefs) {
        if (this.prefs.hasOwnProperty(pref)) {
            this.prefs[pref].current = localStorage.getItem("pref_" + pref) ?? this.prefs[pref].default;
        }
    }
}

/**
 * Gets a preference by name
 * @param prefName The name of the preference to get
 * @param options Optionally, a set of options to choose from. The best option according to the current preference will
 * be picked
 * @returns The chosen preference. If the options parameter is supplied, it will be one of the supplied options, else it
 * will be the preferred option.
 */
UserPreferences.prototype.getPref = function(prefName, options=[]) {
    if (options.length > 0) {
        return this.prefs[prefName].findBestOption(options, this.getPref(prefName))
    } else {
        return this.prefs[prefName].current ?? this.prefs[prefName].default;
    }
}

/**
 * Stores a preference. Does not update the UI
 * @param prefName The name of the preference to save
 * @param prefValue The value of the preference to save
 */
UserPreferences.prototype.setPref = function(prefName, prefValue) {
    this.prefs[prefName].current = prefValue;
    if ("allowSavePref" in this.prefs[prefName]) {
        if (this.prefs[prefName].allowSavePref(prefValue)) {
            window.localStorage.setItem("pref_" + prefName, prefValue);
        }
    } else {
        window.localStorage.setItem("pref_" + prefName, prefValue);
    }
}

/**
 * Applies the preference with the given value, without saving it (see `UserPreference.setPref` for saving)
 *
 * This currently does two things:
 *
 * 1. Sets a `${prefName}--${prefValue} class on the body element and removes old ones
 * 2. Shows and hides elements with the `data-relevant-${prefName}` attribute matching or not matching the value respectively
 *
 * @param prefName Name of the preference to save
 * @param prefValue Value of the preference to save
 */
UserPreferences.prototype.applyPreference = function(prefName, prefValue) {
    let classesToRemove = [];
    for (const clazz of document.body.classList) {
        if (clazz.startsWith(prefName + "--")) {
            classesToRemove.push(clazz);
        }
    }
    if (classesToRemove.length > 0) {
        document.body.classList.remove(classesToRemove);
    }
    document.body.classList.add(prefName + "--" + prefValue);

    if (prefValue) {
        // Show and hide elements with data-relevant-${prefName} values matching/not matching the current prefValue respectively
        let showElements = document.querySelectorAll(`*[data-relevant-${prefName}=${prefValue}]`);
        for (const el of showElements) {
            el.style.display = null;
        }
    }

    let hideElements = [];
    if (prefValue) {
        hideElements = document.querySelectorAll( `*[data-relevant-${prefName}]:not([data-relevant-${prefName}=${prefValue}])`);
    } else {
        hideElements = document.querySelectorAll( `*[data-relevant-${prefName}]`);
    }

    for (const el of hideElements) {
        el.style.display = "none";
    }

}

/**
 * Adds "change" listeners to input elements which control user preferences to update them
 */
UserPreferences.prototype.addInputListeners = function() {
    let self = this;
    for (const el of document.querySelectorAll("*[data-pref-id]")) {
        const prefName = el.dataset.prefId;
        if (el instanceof HTMLSelectElement) {
            el.addEventListener("change", (e) => {
                const prefValue = e.target.selectedOptions[0].value;
                self.setPref(prefName, prefValue);
                self.applyPreference(prefName, prefValue)
            });
        }
    }
}

/**
 * Update the values of all input elements that control user preferences with the current value
 */
UserPreferences.prototype.updatePreferenceInputs = function() {
    // Find all elements with data-pref-id set, and update the values to match the user's preference
    for (const el of document.querySelectorAll("*[data-pref-id]")) {
        let pref = el.dataset.prefId
        if (pref in this.prefs) {
            // <select> … </select> element
            if (el instanceof HTMLSelectElement) {
                let options = [];
                for (const option of el.options) {
                    options.push(option.value);
                }
                el.value = this.getPref(pref, options);
                this.applyPreference(pref, el.value);
            }
        }
    }
}

window.user_prefs = new UserPreferences();
user_prefs.loadPrefs();

document.addEventListener("DOMContentLoaded", () => {
    user_prefs.addInputListeners();
    user_prefs.updatePreferenceInputs();
})
