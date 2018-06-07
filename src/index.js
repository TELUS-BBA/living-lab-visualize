import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';
import registerServiceWorker from './registerServiceWorker';
import '@tds/core-css-reset/dist/index.css'

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
