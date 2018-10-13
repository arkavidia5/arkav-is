<template>
  <div class="navbar">
    <div class="logo">Arkavidia</div>
    <ul>
      <li><a href="#">Lomba</a></li>
      <li><a href="#">Seminar</a></li>
      <li><a href="#">Tim</a></li>
      <li><a href="#">username</a></li>
    </ul>
  </div>
</template>

<script>
  export default {
    data: () => ({})
  }
</script>

<style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    margin-bottom: 24px;
  }

  .logo {
    margin-right: 16px;
  }

  .navbar > ul {
    display: flex;
    list-style: none;
    flex-wrap: wrap;
    padding: 0;
  }

  .navbar > ul > li {
    margin-right: 2.4vw;
  }

  .navbar > ul > li:last-child {
    margin-right: 0;
  }

  .navbar > ul > li > a {
    font-weight: bold;
    font-size: 16px;
    color: var(--v-primary-base, #555);
  }

  .navbar > ul > li > a:hover {
    transition: 0.2s;
  }

  .navbar > ul > li > a::before {
    border-bottom: 0px solid;
  }

  .navbar > ul > li > a:hover::before {
    transition: 0.2;
    border-bottom: 6px solid;
    border-bottom-color: var(--v-primary-base, #1976d2);
  }

  .logo {
    font-weight: bold;
    text-transform: uppercase;
    font-size: 20px;
  }
</style>