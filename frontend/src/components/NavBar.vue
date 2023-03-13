<template>
    <div id="NavBar">
        <ul>
            <router-link
                class="link"
                v-for="page in pages"
                :to="page.link" >
                <button>
                    {{ page.label }}
                </button>
            </router-link>
        </ul>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
    data() {
        return {
            pages: [
                {
                    link: '/',
                    label: 'Servers',
                    view: 'ServersView'
                },
                {
                    link: '/',
                    label: 'Servers',
                    view: 'ServersView'
                },
                {
                    link: '/',
                    label: 'Servers',
                    view: 'ServersView'
                },
                {
                    link: '/',
                    label: 'Servers',
                    view: 'ServersView'
                },
                {
                    link: '/',
                    label: 'Servers',
                    view: 'ServersView'
                },
                {
                    link: '/',
                    label: 'Servers',
                    view: 'ServersView'
                },
            ]
        }
    }
}
</script>

<style scoped>
#NavBar {
  background-color: var(--bg-color);
  overflow: clip;
}
ul {
    margin: 1rem 0 0 0 ;
    padding: 0;
}
.link {
    display: block;
    /* height: 30px; */
    margin: auto;
    width: 90%;
}
</style>