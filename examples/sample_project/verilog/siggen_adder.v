// 8-bit Ripple Carry Adder - Signal Generator Test Design
// Used to generate sweep reports across voltage and frequency corners

module siggen_adder (
    input  wire       clk,
    input  wire       rst,
    input  wire [7:0] a,
    input  wire [7:0] b,
    output reg  [8:0] sum
);

    always @(posedge clk or posedge rst) begin
        if (rst)
            sum <= 9'b0;
        else
            sum <= a + b;
    end

endmodule
