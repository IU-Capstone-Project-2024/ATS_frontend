<template>
    <div class="decision-display">
        <h2>Last Vote Time: {{ decision.last_vote_time }}</h2>
        <ul>
            <li>ML1: {{ decision.ml1 }}</li>
            <li>ML2: {{ decision.ml2 }}</li>
            <li>Algo: {{ decision.algo }}</li>
            <li>Result: {{ decision.result }}</li>
        </ul>
        <a href="https://google.com">View Results</a>
    </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue';

export default {
    name: 'DecisionDisplay',
    setup() {
        const decision = ref({});

        const fetchDecision = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/decisions');
                console.log('Decisions API response:', response.data);
                decision.value = response.data;
            } catch (error) {
                console.error("There was an error!", error);
            }
        };


        onMounted(() => {
            fetchDecision();
        });

        return {
            decision
        };
    }
};
</script>

<style scoped>
.a {
    color: blue
}

.decision-display {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    margin: 20px;
}

.decision-display h2 {
    color: #2c3e50;
}

.decision-display ul {
    list-style-type: none;
    padding: 0;
}

.decision-display li {
    margin: 5px 0;
}
</style>