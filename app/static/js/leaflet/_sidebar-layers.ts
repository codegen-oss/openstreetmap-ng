import { Tooltip } from "bootstrap"
import * as L from "leaflet"
import { mapQueryAreaMaxSize, noteQueryAreaMaxSize } from "../_config"
import { type LayerId, getBaseLayerById, getLayerData, getOverlayLayerById } from "./_layers"
import { cloneTileLayer, getMapBaseLayerId } from "./_map-utils"
import { type SidebarToggleControl, getSidebarToggleButton } from "./_sidebar-toggle-button"
import { getLatLngBoundsSize } from "./_utils"

const minimapZoomOut = 2

export const getLayersSidebarToggleButton = (): SidebarToggleControl => {
    const control = getSidebarToggleButton("layers", "javascripts.map.layers.title")
    const controlOnAdd = control.onAdd

    control.onAdd = (map: L.Map): HTMLElement => {
        const container = controlOnAdd(map)
        const button = container.querySelector("button")

        const minimaps: L.Map[] = []
        const sidebar = control.sidebar
        const layerContainers: NodeListOf<HTMLElement> = sidebar.querySelectorAll(".layer")
        const overlayCheckboxes: NodeListOf<HTMLInputElement> = sidebar.querySelectorAll("input.overlay")

        // Ensure minimaps have been initialized
        const ensureMinimapsInitialized = (): void => {
            if (minimaps.length) return

            for (const container of layerContainers) {
                const layerId = container.dataset.layerId as LayerId
                const layer = getBaseLayerById(layerId)
                if (!layer) {
                    console.error("Base layer", layerId, "not found")
                    continue
                }

                console.debug("Initializing minimap for layer", layerId)
                const minimapContainer: HTMLElement = container.querySelector(".leaflet-container")
                const minimap = L.map(minimapContainer, {
                    attributionControl: false,
                    zoomControl: false,
                    boxZoom: false,
                    doubleClickZoom: false,
                    dragging: false,
                    keyboard: false,
                    scrollWheelZoom: false,
                    touchZoom: false,
                })

                minimap.addLayer(cloneTileLayer(layer))
                minimaps.push(minimap)
            }
        }

        button.addEventListener("click", () => {
            // On sidebar shown, update the sidebar state
            // Skip updates if the sidebar is hidden
            if (!button.classList.contains("active")) return

            ensureMinimapsInitialized()
            const center = map.getCenter()
            const zoom = Math.max(map.getZoom() - minimapZoomOut, 0)

            for (const minimap of minimaps) {
                minimap.setView(center, zoom, { animate: false })
            }

            onMapZoomEnd()
        })

        map.addEventListener("baselayerchange", () => {
            // On base layer change, update the active container
            const activeLayerId = getMapBaseLayerId(map)
            for (const container of layerContainers) {
                const layerId = container.dataset.layerId
                container.classList.toggle("active", layerId === activeLayerId)
            }
        })

        map.addEventListener("overlayadd", ({ name }) => {
            // On overlay layer add, check the corresponding checkbox
            for (const overlayCheckbox of overlayCheckboxes) {
                if (overlayCheckbox.value !== name) continue
                if (overlayCheckbox.checked !== true) {
                    overlayCheckbox.checked = true
                    overlayCheckbox.dispatchEvent(new Event("change"))
                }
                break
            }
        })

        map.addEventListener("overlayremove", ({ name }) => {
            // On overlay layer remove, uncheck the corresponding checkbox
            for (const overlayCheckbox of overlayCheckboxes) {
                if (overlayCheckbox.value !== name) continue
                if (overlayCheckbox.checked !== false) {
                    overlayCheckbox.checked = false
                    overlayCheckbox.dispatchEvent(new Event("change"))
                }
                break
            }
        })

        map.addEventListener("zoomend moveend", () => {
            // On map zoomend or moveend, update the minimaps view
            // Skip updates if the sidebar is hidden
            if (!button.classList.contains("active")) return

            const center = map.getCenter()
            const zoom = Math.max(map.getZoom() - minimapZoomOut, 0)
            for (const minimap of minimaps) {
                minimap.setView(center, zoom)
            }
        })

        // On map zoomend, update the available overlays
        const onMapZoomEnd = () => {
            // Skip updates if the sidebar is hidden
            if (!button.classList.contains("active")) return

            const currentViewAreaSize = getLatLngBoundsSize(map.getBounds())

            for (const overlayCheckbox of overlayCheckboxes) {
                let areaMaxSize: number
                const layerId = overlayCheckbox.value
                switch (layerId) {
                    case "notes":
                        areaMaxSize = noteQueryAreaMaxSize
                        break
                    case "data":
                        areaMaxSize = mapQueryAreaMaxSize
                        break
                    default:
                        // Some overlays are always available
                        continue
                }

                const isAvailable = currentViewAreaSize <= areaMaxSize
                if (isAvailable) {
                    if (overlayCheckbox.disabled) {
                        overlayCheckbox.disabled = false

                        const parent: HTMLElement = overlayCheckbox.closest(".form-check")
                        parent.classList.remove("disabled")
                        parent.ariaDisabled = "false"
                        const tooltip = Tooltip.getInstance(parent)
                        tooltip.disable()
                        tooltip.hide()

                        // Restore the overlay state if it was checked before
                        if (overlayCheckbox.dataset.wasChecked) {
                            console.debug("Restoring checked state for overlay", layerId)
                            overlayCheckbox.dataset.wasChecked = undefined
                            overlayCheckbox.checked = true
                            overlayCheckbox.dispatchEvent(new Event("change"))
                        }
                    }
                } else if (!overlayCheckbox.disabled) {
                    overlayCheckbox.blur()
                    overlayCheckbox.disabled = true

                    const parent: HTMLElement = overlayCheckbox.closest(".form-check")
                    parent.classList.add("disabled")
                    parent.ariaDisabled = "true"
                    Tooltip.getOrCreateInstance(parent, {
                        title: parent.dataset.bsTitle,
                        placement: "top",
                    }).enable()

                    // Force uncheck the overlay when it becomes unavailable
                    if (overlayCheckbox.checked) {
                        console.debug("Forcing unchecked state for overlay", layerId)
                        overlayCheckbox.dataset.wasChecked = "true"
                        overlayCheckbox.checked = false
                        overlayCheckbox.dispatchEvent(new Event("change"))
                    }
                }
            }
        }
        map.addEventListener("zoomend", onMapZoomEnd)

        // On layer click, update the active (base) layer
        const onBaseLayerClick = (e: Event) => {
            const layerContainer = e.currentTarget as HTMLElement
            const layerId = layerContainer.dataset.layerId as LayerId
            const layer = getBaseLayerById(layerId)
            if (!layer) {
                console.error("Base layer", layerId, "not found")
                return
            }

            // Skip updates if the layer is already active
            const activeLayerId = getMapBaseLayerId(map)
            if (layerId === activeLayerId) return

            // Remove all base layers
            map.eachLayer((layer) => {
                const data = getLayerData(layer)
                if (data && getBaseLayerById(data.layerId)) {
                    console.debug("Removing base layer", data.layerId)
                    map.removeLayer(layer)
                }
            })

            // Add the new base layer
            console.debug("Adding base layer", layerId)
            map.addLayer(layer)

            // Trigger the baselayerchange event
            // https://leafletjs.com/reference.html#map-baselayerchange
            // https://leafletjs.com/reference.html#layerscontrolevent
            map.fire("baselayerchange", { layer, name: layerId })
        }
        for (const layerContainer of layerContainers) {
            layerContainer.addEventListener("click", onBaseLayerClick)
        }

        // On overlay checkbox change, add or remove the overlay layer
        const onOverlayCheckboxChange = (e: Event) => {
            const overlayCheckbox = e.currentTarget as HTMLInputElement
            const layerId = overlayCheckbox.value as LayerId
            const layer = getOverlayLayerById(layerId)
            if (!layer) {
                console.error("Overlay layer", layerId, "not found")
                return
            }

            const checked = overlayCheckbox.checked
            const containsLayer = map.hasLayer(layer)

            // Skip updates if the layer is already in the correct state
            if (checked === containsLayer) {
                console.warn("Overlay layer", layerId, "is already", checked ? "added" : "removed")
                return
            }

            // Add or remove the overlay layer
            if (checked) {
                console.debug("Adding overlay layer", layerId)
                map.addLayer(layer)

                // Trigger the overlayadd event
                // https://leafletjs.com/reference.html#map-overlayadd
                // https://leafletjs.com/reference.html#layerscontrolevent
                map.fire("overlayadd", { layer, name: layerId })
            } else {
                console.debug("Removing overlay layer", layerId)
                map.removeLayer(layer)

                // Trigger the overlayremove event
                // https://leafletjs.com/reference.html#map-overlayremove
                // https://leafletjs.com/reference.html#layerscontrolevent
                map.fire("overlayremove", { layer, name: layerId })
            }
        }
        for (const overlayCheckbox of overlayCheckboxes) {
            overlayCheckbox.addEventListener("change", onOverlayCheckboxChange)
        }

        return container
    }

    return control
}
