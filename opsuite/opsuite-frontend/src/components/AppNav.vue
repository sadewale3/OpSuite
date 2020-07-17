<template>
  <nav>
    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>OpSuite</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app clipped>
      <v-list>
        <v-list-group
          v-for="item in items"
          :key="item.title"
          v-model="item.active"
          :prepend-icon="item.icon"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="subItem in item.items"
            :key="subItem.title"
            router
            :to="subItem.route"
            link
          >
            <v-list-item-content>
              <v-list-item-title v-text="subItem.title"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
export default {
  name: "AppNav",
  data: () => ({
    drawer: null,
    items: [
      {
        active: true,
        icon: "mdi-account-key",
        title: "A.F.I.S.H.",
        items: [
          { title: "Jobs", route: "/afish/jobs" },
          { title: "Executions", route: "/afish/executions" },
          { title: "Audit Logs", route: "/afish/auditlogs" }
        ]
      }
    ],
    model: 1
  })
};
</script>
