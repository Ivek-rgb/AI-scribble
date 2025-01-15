
/** @typedef {Object} AppState
 * @prop {string} loadedModel
 * @prop {{value: string, label: string}[]} availableModels
 * @prop {boolean} modelsBeingRefreshed
 * @prop {boolean} guessing
 * @prop {string | null} guessPromiseUUID
  */


/** @type {AppState} */
export let appState = $state({
  loadedModel: '',
  availableModels: [],
  modelsBeingRefreshed: false,
  guessing: false,
  guessPromiseUUID: null
});
