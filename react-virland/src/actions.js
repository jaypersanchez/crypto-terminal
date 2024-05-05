// Action Types
export const SET_SELECTED_VALUE = 'SET_SELECTED_VALUE';

// Action Creator
export function setSelectedValue(value) {
  return {
    type: SET_SELECTED_VALUE,
    payload: value
  };
}
