<template>
  <div>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="formData.name" id="name" required />
      </div>
      <div>
        <label for="birth-date">Birth Date:</label>
        <input type="date" v-model="formData.birth_date" id="birth-date" required />
      </div>
      <div>
        <label for="gender">Gender:</label>
        <input type="text" v-model="formData.gender" id="gender" required />
      </div>
      <div>
        <label for="job">Job:</label>
        <input type="text" v-model="formData.job" id="job" required />
      </div>
      <div>
        <label for="hobby">Hobby:</label>
        <input type="text" v-model="formData.hobby" id="hobby" required />
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        name: '',
        birth_date: '',
        gender: '',
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

