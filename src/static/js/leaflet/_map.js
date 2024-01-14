import * as L from "leaflet"
import { getBaseLayerById, getOverlayLayerById } from "./_layers.js"

/**
 * Get the main map
 * @param {HTMLElement} container The container element
 * @returns {L.Map} The map
 */
const getMainMap = (container) => {
    const map = L.map(container, {})

    // Disable Leaflet's attribution prefix
    map.attributionControl.setPrefix(false)

    // Configure layers
    const gpsLayer = getOverlayLayerById("gps")
    const dataLayer = getOverlayLayerById("data")
    const noteLayer = getOverlayLayerById("note")

    // TODO: finish configuration
    // TOOD: get/set last state
    // TODO: map.invalidateSize({ pan: false }) on sidebar-content

    // On layer add, limit max zoom if it's a base layer
    const onLayerAdd = ({ layer }) => {
        if (getBaseLayerById(layer.options.layerId)) {
            map.setMaxZoom(layer.options.maxZoom)
        }
    }

    // Listen for events
    map.addEventListener("layeradd", onLayerAdd)

    return map
}
