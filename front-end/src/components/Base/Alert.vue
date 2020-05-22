<template>
    <div class="alert" role="alert" :class="'alert-' + variant">
        {{ message }}
    </div>
</template>

<script>
export default {
    props: ['variant', 'message']
}
</script>

