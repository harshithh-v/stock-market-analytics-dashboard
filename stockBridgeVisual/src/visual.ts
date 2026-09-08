"use strict";

import powerbi from "powerbi-visuals-api";
import { FormattingSettingsService } from "powerbi-visuals-utils-formattingmodel";
import "./../style/visual.less";

import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
import IVisualEventService = powerbi.extensibility.IVisualEventService;

import { VisualFormattingSettingsModel } from "./settings";

export class Visual implements IVisual {

    private events: IVisualEventService;
    private target: HTMLElement;
    private formattingSettings: VisualFormattingSettingsModel;
    private formattingSettingsService: FormattingSettingsService;

    private symbolText: HTMLDivElement;

    constructor(options: VisualConstructorOptions) {

        this.events = options.host.eventService;
        this.formattingSettingsService =
            new FormattingSettingsService();

        this.target = options.element;

        // Remove all default content
        this.target.innerHTML = "";

        // Remove spacing from the visual container
        this.target.style.padding = "0";
        this.target.style.margin = "0";
        this.target.style.width = "100%";
        this.target.style.height = "100%";
        this.target.style.overflow = "hidden";

        // Company symbol text
        this.symbolText = document.createElement("div");

        this.symbolText.innerText = "NONE";

        this.symbolText.style.fontSize = "24px";
        this.symbolText.style.fontWeight = "bold";
        this.symbolText.style.textAlign = "center";
        this.symbolText.style.margin = "0";
        this.symbolText.style.padding = "0";
        this.symbolText.style.lineHeight = "1";
        this.symbolText.style.width = "100%";

        this.target.appendChild(this.symbolText);
    }

    public update(options: VisualUpdateOptions) {

        this.events.renderingStarted(options);

        try {

            console.log("Visual update:", options);

            let symbol = "";

            if (
                options.dataViews &&
                options.dataViews.length > 0 &&
                options.dataViews[0].table &&
                options.dataViews[0].table.rows &&
                options.dataViews[0].table.rows.length > 0
            ) {

                const row = options.dataViews[0].table.rows[0];

                if (
                    row.length > 0 &&
                    row[0] !== null &&
                    row[0] !== undefined
                ) {

                    symbol = String(row[0])
                        .trim()
                        .toUpperCase();
                }
            }

            // No company selected
            if (!symbol) {

                this.symbolText.innerText = "NONE";

                this.events.renderingFinished(options);

                return;
            }

            // Display only the company symbol
            this.symbolText.innerText = symbol;

            // Send symbol to Python bridge
            const bridgeUrl =
                "http://localhost:8000/symbol?symbol=" +
                encodeURIComponent(symbol);

            console.log(
                "Calling Python bridge:",
                bridgeUrl
            );

            fetch(bridgeUrl, {
                method: "GET"
            })
                .then(response => {

                    if (!response.ok) {

                        throw new Error(
                            "Bridge returned HTTP " +
                            response.status
                        );
                    }

                    return response.text();
                })
                .then(result => {

                    console.log(
                        "Python bridge response:",
                        result
                    );

                })
                .catch(error => {

                    console.error(
                        "Could not connect to Python bridge:",
                        error
                    );

                });

            this.events.renderingFinished(options);

        }
        catch (error) {

            console.log(
                "Error in update method:",
                error
            );

            this.symbolText.innerText = "ERROR";

            this.events.renderingFailed(
                options,
                String(error)
            );
        }
    }

    public getFormattingModel():
        powerbi.visuals.FormattingModel {

        return this.formattingSettingsService
            .buildFormattingModel(
                this.formattingSettings
            );
    }
}