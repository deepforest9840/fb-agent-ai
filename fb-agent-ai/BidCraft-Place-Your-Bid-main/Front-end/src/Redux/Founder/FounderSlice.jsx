import { createSlice } from "@reduxjs/toolkit";


const initialState = {
    founder: null,
    loading: false,
    error: false,
};

const founderSlice = createSlice({
    name: "founder",
    initialState,
    reducers: {
        founderStart: (state) => {
            state.loading = true;
        },
        founderSuccess: (state, action) => {
            state.founder = action.payload;
            state.loading = false;
            state.error = false;
        },
        founderFailure: (state , action) => {
            state.loading = false;
            state.error = action.payload;
        },
        // logout: (state) => {
        //     state.currentUser = null;
        //     state.loading = false;
        //     state.error = false;
        // },
        founderSignout: (state) => {
            state.founder = null;
            state.loading = false;
            state.error = false;
        },

    },
    
});

export const {founderStart , founderSuccess , founderFailure , founderSignout} = founderSlice.actions;
export default founderSlice.reducer;