import { describe, expect, it } from "vitest";

describe("frontend test setup", () => {
  it("runs in jsdom", () => {
    const node = document.createElement("div");
    node.textContent = "ok";
    document.body.append(node);

    expect(document.body.textContent).toContain("ok");
  });
});
