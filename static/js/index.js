class Pager {
    constructor({count, api, last=0}) {
        this.count = count;
        this.last = last;
        this.api = api;
    }

    next(callback) {
        if (this.last === null) {
            return;
        }
        Request.get(this.api, {count: this.count, last: this.last})
            .then(resp => {
                this.last = resp.next_value;
                callback(resp);
            });
    }
}
class IndexComponent {
    constructor({indexBoxId, poemCountId}) {
        this.indexBox = document.getElementById(indexBoxId);
        this.indexBox.innerHTML = '';
        this.poemCount = document.getElementById(poemCountId);

        this.pager = new Pager({count: 10, api: '/api/poem/'});
        this.pager.next(this.display.bind(this));

        this.indexBox.addEventListener('scroll', this.scrollListener.bind(this));
    }

    display(resp) {
        if (this.pager.last === null) {
            this.indexBox.removeEventListener('scroll', this.scrollListener.bind(this));
        }
        this.poemCount.innerText = resp.total_count;

        let poemList = resp.object_list;
        let indexItemTemplate = template`
        <a href="${2}">
            <div class="index-box__item-box">
                <div class="index-box__title">${0}</div>
                <div class="index-box__time">${1}</div>
            </div>
        </a>`;

        for (let poem of poemList) {
            let html = stringToHtml(indexItemTemplate(
                poem.title,
                new Time({timestamp: poem.create_time}).relative,
                `/writer/@${poem.id}`,
            ));
            this.indexBox.appendChild(html);
        }
    }

    scrollListener() {
        if (this.indexBox.scrollHeight - this.indexBox.clientHeight - this.indexBox.scrollTop < 55 * 5) {
            this.pager.next(this.display.bind(this));
        }
    }
}