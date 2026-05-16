import { Component, OnInit, Input, ElementRef, ViewEncapsulation } from '@angular/core';
import { DataService } from '../../../services/data.service';
import { Technique, Tactic, Note } from '../../../classes/stix';
import { ViewModel, TechniqueVM } from '../../../classes';
import { ViewModelsService } from '../../../services/viewmodels.service';
import { CellPopover } from '../cell-popover';

@Component({
    selector: 'app-tooltip',
    templateUrl: './tooltip.component.html',
    styleUrls: ['./tooltip.component.scss'],
    encapsulation: ViewEncapsulation.None,
})
export class TooltipComponent extends CellPopover implements OnInit {
    @Input() technique: Technique;
    @Input() tactic: Tactic;
    @Input() viewModel: ViewModel;
    @Input() tooltipStyle: any;
    public placement: string;
    public notes: Note[];

    public get isCellPinned(): boolean {
        return this.viewModelsService.pinnedCell === this.techniqueVM.technique_tactic_union_id;
    }

    public get techniqueVM(): TechniqueVM {
        return this.viewModel.getTechniqueVM(this.technique, this.tactic);
    }

    constructor(
        public element: ElementRef,
        public dataService: DataService,
        public viewModelsService: ViewModelsService
    ) {
        super(element);
    }

    ngOnInit() {
        this.placement = this.getPlacement();
        let domain = this.dataService.getDomain(this.viewModel.domainVersionID);
        this.notes = domain.notes.filter((note) => {
            return note.object_refs.includes(this.technique.id);
        });
    }

    public getPlacement(): string {
        return this.getPosition();
    }

    public unpin(): void {
        this.viewModelsService.pinnedCell = '';
    }

    public forwardClick(event: MouseEvent): void {
        const tooltipElement = this.element.nativeElement.querySelector('.tooltip') as HTMLElement;
        if (!tooltipElement) return;

        tooltipElement.style.pointerEvents = 'none';
        const target = document.elementFromPoint(event.clientX, event.clientY) as HTMLElement;
        tooltipElement.style.pointerEvents = '';

        const techniqueCell = target?.closest('technique-cell .technique-cell > div') as HTMLElement;
        if (techniqueCell) {
            techniqueCell.dispatchEvent(
                new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    clientX: event.clientX,
                    clientY: event.clientY,
                    shiftKey: event.shiftKey,
                    ctrlKey: event.ctrlKey,
                    metaKey: event.metaKey,
                })
            );
        }
    }
}
