import { createStore, combineReducers } from 'redux';
import selectionReducer from './reducer';

const rootReducer = combineReducers({
  selection: selectionReducer
});

const store = createStore(rootReducer);

export default store;
