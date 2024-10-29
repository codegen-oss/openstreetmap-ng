import { Tooltip } from "bootstrap"
import i18next from "i18next"
import * as L from "leaflet"

const zoomAcceleration = 3

export const getZoomControl = () => {
    const control = new L.Control()
    let controlMap: L.Map | null = null

    /** On zoom change, disable/enable specific buttons */
    const onMapZoomChange = (): void => {
        const container = control.getContainer()
        const zoomInButton: HTMLButtonElement = container.querySelector("button.zoom-in-btn")
        const zoomOutButton: HTMLButtonElement = container.querySelector("button.zoom-out-btn")

        const currentZoom = controlMap.getZoom()
        const minZoom = controlMap.getMinZoom()
        const maxZoom = controlMap.getMaxZoom()

        // Enable/disable buttons based on current zoom level
        if (currentZoom <= minZoom) {
            zoomOutButton.blur()
            zoomOutButton.disabled = true
        } else {
            zoomOutButton.disabled = false
        }

        if (currentZoom >= maxZoom) {
            zoomInButton.blur()
            zoomInButton.disabled = true
        } else {
            zoomInButton.disabled = false
        }
    }

    control.onAdd = (map: L.Map): HTMLElement => {
        if (controlMap) {
            console.error("ZoomControl has already been added to the map")
            return
        }
        controlMap = map

        // Create container
        const container = document.createElement("div")
        container.className = "leaflet-control zoom"

        // Create buttons and tooltips
        const zoomInText = i18next.t("javascripts.map.zoom.in")
        const zoomInButton = document.createElement("button")
        zoomInButton.className = "zoom-in-btn control-button"
        zoomInButton.ariaLabel = zoomInText
        zoomInButton.innerHTML = "<span class='icon zoom-in'></span>"
        container.appendChild(zoomInButton)

        new Tooltip(zoomInButton, {
            title: zoomInText,
            placement: "left",
        })

        const zoomOutText = i18next.t("javascripts.map.zoom.out")
        const zoomOutButton = document.createElement("button")
        zoomOutButton.className = "zoom-out-btn control-button"
        zoomOutButton.ariaLabel = zoomOutText
        zoomOutButton.innerHTML = "<span class='icon zoom-out'></span>"
        container.appendChild(zoomOutButton)

        new Tooltip(zoomOutButton, {
            title: zoomOutText,
            placement: "left",
        })

        const getZoomSpeed = ({ altKey, shiftKey }: MouseEvent): number => (altKey || shiftKey ? zoomAcceleration : 1)
        zoomInButton.addEventListener("click", (e) => map.zoomIn(getZoomSpeed(e)))
        zoomOutButton.addEventListener("click", (e) => map.zoomOut(getZoomSpeed(e)))

        // Listen for events
        map.addEventListener("zoomend zoomlevelschange", onMapZoomChange)
        // Initial update to set button states
        onMapZoomChange()

        return container
    }

    return control
}
