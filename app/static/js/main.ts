import "./_tracking"

import "./_i18n"

import "./_fixthemap"
import "./_id"
import "./_rapid"
import "./_welcome"
import { configureMainMap } from "./leaflet/_main-map"
import "./messages/_index"
import "./messages/_new"
import "./oauth2/_response-form-post"
import "./settings/_email"
import "./settings/_index"
import "./settings/_security"
import "./settings/applications/_edit"
import "./settings/applications/_index"
import "./traces/_details"
import "./traces/_edit"
import "./traces/_list"
import "./traces/_preview"
import "./traces/_upload"
import "./user/_account-confirm"
import "./user/_login"
import "./user/_profile"
import "./user/_reset-password"
import "./user/_signup"
import "./user/_terms"

const mapContainer = document.querySelector("div.main-map")
if (mapContainer) configureMainMap(mapContainer)

import "./_bootstrap"
import "./_copy-group"
import "./_rich-text"
