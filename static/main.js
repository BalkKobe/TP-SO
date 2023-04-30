const app = new Vue({
    el: '#app',
    data: {
      titulo: 'Prueba',
    },
    methods: {
      mostrarTabla(tabla) {
        axios
          .get(`http://localhost:5000/${tabla}`)
          .then((response) => {
            this.titulo = tabla.charAt(0).toUpperCase() + tabla.slice(1);
            console.log(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
      },
    },
  });