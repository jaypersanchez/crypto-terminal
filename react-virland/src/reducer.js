import { SET_SELECTED_VALUE } from './actions';

const initialState = {
  selectedValue: ''
};

function selectionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_SELECTED_VALUE:
      return {
        ...state,
        selectedValue: action.payload
      };
    default:
      return state;
  }
}

export default selectionReducer;
