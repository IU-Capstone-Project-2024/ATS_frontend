<template>
    <div class="decision-display">
        <h2>Last Vote Time: {{ decision.last_vote_time }}</h2>
        <div class="decisions">
            <div class="decision">
                <span>ML1</span>
                <button :class="decision.ml1">{{ decision.ml1 }}</button>
            </div>
            <div class="decision">
                <span>ML2</span>
                <button :class="decision.ml2">{{ decision.ml2 }}</button>
            </div>
            <div class="decision">
                <span>Algo</span>
                <button :class="decision.algo">{{ decision.algo }}</button>
            </div>
            <div class="decision">
                <span>Result</span>
                <button :class="decision.result">{{ decision.result }}</button>
            </div>
        </div>
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
    text-align: center;
}

.decision-display h2 {
    color: #2c3e50;
    margin-bottom: 20px;
}

.decisions {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}

.decision {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.decision span {
    margin-bottom: 10px;
    font-size: 1.2em;
    font-weight: bold;
    color: #2c3e50;
}

.decision button {
    padding: 20px 40px;
    border: none;
    border-radius: 10px;
    font-size: 1.5em;
    font-weight: bold;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease;
    min-width: 200px;
    /* Ensure buttons have a minimum width */
}

.sell {
    background-color: red;
}

.buy {
    background-color: green;
}

.hold {
    background-color: orange;
}

.sell:hover,
.buy:hover,
.hold:hover {
    opacity: 0.8;
}
</style>
