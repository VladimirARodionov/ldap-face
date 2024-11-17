import React from "react";
import ReactDOM from "react-dom/client";
import { HashRouter } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "primereact/resources/themes/lara-light-cyan/theme.css";
import { PrimeReactProvider } from 'primereact/api';
import App from "./App";

// Creating the root application component
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
  <PrimeReactProvider>
    <HashRouter>
      <App />
    </HashRouter>
  </PrimeReactProvider>
  </React.StrictMode>
);
