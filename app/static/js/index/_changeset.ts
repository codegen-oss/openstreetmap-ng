import i18next from "i18next"
import type * as L from "leaflet"
import { renderColorPreviews } from "../_color-preview"
import { configureStandardForm } from "../_standard-form"
import { getPageTitle } from "../_title"
import type { Bounds, OSMChangeset } from "../_types"
import { focusMapObject } from "../leaflet/_focus-layer"
import { makeBoundsMinimumSize } from "../leaflet/_utils"
import { getBaseFetchController } from "./_base-fetch"
import type { IndexController } from "./_router"

// app/format/element_list.py
interface ChangesetListEntry {
    type: string
    id: number
    name?: string
    icon?: string
    // biome-ignore lint/style/useNamingConvention: <explanation>
    icon_title?: string
    version: number
    visible: boolean
}

const elementsPerPage = 20
const paginationDistance = 2

/** Create a new changeset controller */
export const getChangesetController = (map: L.Map): IndexController => {
    let paramsId: number | null = null
    let paramsBounds: Bounds[] | null = null

    /** On map zoom change, refocus the changeset (due to size change) */
    const onMapZoomEnd = (e?: L.LeafletEvent): void => {
        const object: OSMChangeset = {
            type: "changeset",
            id: paramsId,
            bounds: paramsBounds.map((b) => makeBoundsMinimumSize(map, b)),
        }
        focusMapObject(map, object, {
            // Fit the bounds only on the initial update
            fitBounds: !e,
        })
    }

    const base = getBaseFetchController(map, "changeset", (sidebarContent) => {
        renderColorPreviews()

        const sidebarTitleElement = sidebarContent.querySelector(".sidebar-title") as HTMLElement
        const sidebarTitle = sidebarTitleElement.textContent
        const elementsSection = sidebarContent.querySelector("div.elements")

        // Set page title
        document.title = getPageTitle(sidebarTitle)

        // Handle not found
        if (!sidebarTitleElement.dataset.params) return

        // Get params
        const params = JSON.parse(sidebarTitleElement.dataset.params)
        paramsId = params.id
        paramsBounds = params.bounds
        const elements: { [key: string]: ChangesetListEntry[] } = params.elements

        // Optionally update on map zoom (not all changesets have bounds)
        if (paramsBounds) {
            // Listen for events and run initial update
            map.addEventListener("zoomend", onMapZoomEnd)
            onMapZoomEnd()
        }

        renderElements(elementsSection, elements)

        /** On success callback, reload the changeset */
        const onFormSuccess = () => {
            controller.unload()
            controller.load({ id: paramsId.toString() })
        }
        const subscriptionForm = sidebarContent.querySelector("form.subscription-form")
        if (subscriptionForm) configureStandardForm(subscriptionForm, onFormSuccess)
        const commentForm = sidebarContent.querySelector("form.comment-form")
        if (commentForm) configureStandardForm(commentForm, onFormSuccess)
    })

    const controller: IndexController = {
        load: ({ id }) => {
            const url = `/api/partial/changeset/${id}`
            base.load({ url })
        },
        unload: () => {
            map.removeEventListener("zoomend", onMapZoomEnd)
            focusMapObject(map, null)
            base.unload()
        },
    }
    return controller
}

/** Render elements component */
const renderElements = (elementsSection: HTMLElement, elements: { [key: string]: ChangesetListEntry[] }): void => {
    console.debug("renderElements")

    const groupTemplate = elementsSection.querySelector("template.group")
    const entryTemplate = elementsSection.querySelector("template.entry")
    const fragment = document.createDocumentFragment()

    for (const type of ["way", "relation", "node"]) {
        const elementsType = elements[type]
        if (elementsType.length) {
            fragment.appendChild(renderElementType(groupTemplate, entryTemplate, type, elementsType))
        }
    }

    if (fragment.children.length) {
        elementsSection.innerHTML = ""
        elementsSection.appendChild(fragment)
    } else {
        elementsSection.remove()
    }
}

/** Render elements of a specific type */
const renderElementType = (
    groupTemplate: HTMLTemplateElement,
    entryTemplate: HTMLTemplateElement,
    type: string,
    elements: ChangesetListEntry[],
): DocumentFragment => {
    console.debug("renderElementType", type, elements)

    const groupFragment = groupTemplate.content.cloneNode(true) as DocumentFragment
    const titleElement = groupFragment.querySelector(".title")
    const tbody = groupFragment.querySelector("tbody")

    // Calculate pagination
    const elementsLength = elements.length
    const totalPages = Math.ceil(elementsLength / elementsPerPage)
    let currentPage = 1

    const updateTitle = (): void => {
        let count: string
        if (totalPages > 1) {
            const from = (currentPage - 1) * elementsPerPage + 1
            const to = Math.min(currentPage * elementsPerPage, elementsLength)
            count = i18next.t("pagination.range", { x: `${from}-${to}`, y: elementsLength })
        } else {
            count = elementsLength.toString()
        }

        // Prefer static translation strings to ease automation
        let newTitle: string
        if (type === "node") {
            // @ts-ignore
            newTitle = i18next.t("browse.changeset.node", { count })
        } else if (type === "way") {
            // @ts-ignore
            newTitle = i18next.t("browse.changeset.way", { count })
        } else if (type === "relation") {
            // @ts-ignore
            newTitle = i18next.t("browse.changeset.relation", { count })
        }
        titleElement.textContent = newTitle
    }

    const updateTable = (): void => {
        const tbodyFragment = document.createDocumentFragment()

        const iStart = (currentPage - 1) * elementsPerPage
        const iEnd = Math.min(currentPage * elementsPerPage, elementsLength)
        for (let i = iStart; i < iEnd; i++) {
            const element = elements[i]

            const entryFragment = entryTemplate.content.cloneNode(true) as DocumentFragment
            const iconImg = entryFragment.querySelector("img")
            const linkLatest = entryFragment.querySelector("a.link-latest")
            const linkVersion = entryFragment.querySelector("a.link-version")

            if (element.icon) {
                iconImg.src = `/static/img/element/${element.icon}`
                iconImg.title = element.icon_title
            } else {
                iconImg.remove()
            }

            if (!element.visible) {
                linkLatest.parentElement.parentElement.classList.add("deleted")
            }

            if (element.name) {
                const bdi = document.createElement("bdi")
                bdi.textContent = element.name
                linkLatest.appendChild(bdi)
                const span = document.createElement("span")
                span.textContent = ` (${element.id})`
                linkLatest.appendChild(span)
            } else {
                linkLatest.textContent = element.id.toString()
            }
            linkLatest.href = `/${type}/${element.id}`
            linkVersion.textContent = `v${element.version}`
            linkVersion.href = `/${type}/${element.id}/history/${element.version}`
            tbodyFragment.appendChild(entryFragment)
        }

        tbody.innerHTML = ""
        tbody.appendChild(tbodyFragment)
    }

    // Optionally configure pagination controls
    if (totalPages > 1) {
        const paginationContainer = groupFragment.querySelector(".pagination")

        const updatePagination = (): void => {
            console.debug("updatePagination", currentPage)

            const paginationFragment = document.createDocumentFragment()

            for (let i = 1; i <= totalPages; i++) {
                const distance = Math.abs(i - currentPage)
                if (distance > paginationDistance && i !== 1 && i !== totalPages) {
                    if (i === 2 || i === totalPages - 1) {
                        const li = document.createElement("li")
                        li.classList.add("page-item", "disabled")
                        li.ariaDisabled = "true"
                        li.innerHTML = `<span class="page-link">...</span>`
                        paginationFragment.appendChild(li)
                    }
                    continue
                }

                const li = document.createElement("li")
                li.classList.add("page-item")

                const button = document.createElement("button")
                button.classList.add("page-link")
                button.textContent = i.toString()
                li.appendChild(button)

                if (i === currentPage) {
                    li.classList.add("active")
                    li.ariaCurrent = "page"
                } else {
                    button.addEventListener("click", () => {
                        currentPage = i
                        updateTitle()
                        updateTable()
                        updatePagination()
                    })
                }

                paginationFragment.appendChild(li)
            }

            paginationContainer.innerHTML = ""
            paginationContainer.appendChild(paginationFragment)
        }

        updatePagination()
    } else {
        groupFragment.querySelector("nav").remove()
    }

    // Initial update
    updateTitle()
    updateTable()

    return groupFragment
}
