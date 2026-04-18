export type CofounderIdea = {
  idea: string;
  tier: "free" | "pro";
};

export const normalizeIdea = (input: string): CofounderIdea => ({
  idea: input.trim(),
  tier: "free",
});
