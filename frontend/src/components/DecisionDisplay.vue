<template>
    <div class="decision-display">
        <h2>Last Vote Time: {{ decision.last_vote_time }}</h2>
        <ul>
            <li>ML1: <span :class="decision.ml1">{{ decision.ml1 }}</span></li>
            <li>ML2: <span :class="decision.ml2">{{ decision.ml2 }}</span></li>
            <li>Algo: <span :class="decision.algo">{{ decision.algo }}</span></li>
            <li>Result: <span :class="decision.result">{{ decision.result }}</span></li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
    name: 'DecisionDisplay',
    setup() {
        const decision = ref({});

        const fetchDecision = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/decisions');
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
.decision-display {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.decision-display h2 {
    color: #2c3e50;
}

.decision-display ul {
    list-style-type: none;
    padding: 0;
    display: flex;
    justify-content: space-between;
}

.decision-display li {
    margin: 5px 0;
}

.sell {
    color: red;
    font-weight: bold;
}

.buy {
    color: green;
    font-weight: bold;
}

.hold {
    color: orange;
    font-weight: bold;
}
</style>