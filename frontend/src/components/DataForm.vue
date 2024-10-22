<template>
  <div>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="name">名称:</label>
        <input type="text" v-model="formData.name" id="name" required />
      </div>
      <div>
        <label for="email">邮箱:</label>
        <input type="email" v-model="formData.email" id="email" required />
      </div>
      <div>
        <label for="password">密码:</label>
        <input type="password" v-model="formData.password" id="password" required />
      </div>
      <div>
        <label for="job">专业:</label>
        <input type="text" v-model="formData.job" id="job" required />
      </div>
      <div>
        <label for="hobby">兴趣:</label>
        <input type="text" v-model="formData.hobby" id="hobby" required />
      </div>
      <button type="submit">提交</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        job: '',
        hobby: ''
      }
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await fetch('http://23.184.88.52:8000/api/data/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        alert('Data submitted successfully');
      } catch (error) {
        alert(`Form submission failed: ${error.message}`);
      }
    }
  }
};
</script>
