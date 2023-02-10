<template>
  <x-star-rating :value="value" number="5"></x-star-rating>
</template>

<script>
import StarRating from "@/components/UI/starrating/starElement";

export default {
  name: "StarRating",
  props: {
    value: {
      type: Number,
      default: 0
    }
  }
}

customElements.define('x-star-rating', StarRating);
</script>

<style scoped>
x-star-rating {
    font-family: 'Ionicons';
    font-size: 12px;
    display: inline-flex;
    cursor: pointer;
}

x-star-rating > .star::after {
    content: '\f3ae';
    color: #777;
}

x-star-rating > .star.full::after {
    content: '\f2fc';
    color: #fd0;
}
</style>