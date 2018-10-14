<template>
  <nav class="navbar">
    <div class="logo">Arkavidia</div>
    <ul>
      <li><a href="#" class="body-link hover-only">Lomba</a></li>
      <li><a href="#" class="body-link hover-only">Seminar</a></li>
      <li><a href="#" class="body-link hover-only">Tim</a></li>
      <li><a href="#" class="body-link hover-only">username</a></li>
    </ul>
  </nav>
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
    color: #555;
  }

  .logo {
    font-weight: bold;
    text-transform: uppercase;
    font-size: 20px;
  }
</style>